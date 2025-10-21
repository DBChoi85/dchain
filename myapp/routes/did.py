# app.py
from flask import Blueprint, request, jsonify, abort
from nacl.signing import SigningKey
from nacl.encoding import RawEncoder
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from jwt import ExpiredSignatureError, InvalidAudienceError
import base58
import json
import os
import stat
import threading
import jwt 
import time
from typing import Tuple


did_api = Blueprint('did', __name__)

# =====================
# Storage configuration
# =====================
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DIDS_DIR = DATA_DIR / "dids"        # DID Documents
KEYS_DIR = DATA_DIR / "keys"        # Private keys (server-only)
INDEX_PATH = DATA_DIR / "index.json" # Metadata index (did -> {created_at,label})

# 파일 상단 import 근처에 넣기

def verify_vc_token(vc_jwt: str, aud: str | None = None):
    """
    VC-JWT 하나를 검증하고 결과 반환.
    Returns: (valid: bool, payload_or_reason: dict|str)
    """
    # 1) iss 추출 (서명검증 없이)
    try:
        unverified = jwt.decode(vc_jwt, options={"verify_signature": False})
        issuer = unverified.get("iss")
        if not issuer:
            return False, "No iss in VC"
    except Exception as e:
        return False, f"malformed token: {e}"

    # 2) DID 문서에서 공개키 로드
    try:
        pk = _load_public_key_from_diddoc(issuer)
    except Exception as e:
        return False, f"issuer key load failed: {e}"

    # 3) 서명/만료/aud 검증
    try:
        payload = jwt.decode(
            vc_jwt,
            pk,
            algorithms=["EdDSA"],
            options={"require": ["iss", "sub", "exp", "nbf", "iat"], "verify_aud": bool(aud)},
            audience=aud if aud else None,
        )
        return True, payload
    except ExpiredSignatureError:
        return False, "expired"
    except InvalidAudienceError:
        return False, "audience mismatch"
    except Exception as e:
        return False, str(e)


# Create dirs at startup
for d in (DIDS_DIR, KEYS_DIR):
    d.mkdir(parents=True, exist_ok=True)

_index_lock = threading.Lock()


def _chmod_600(p: Path) -> None:
    try:
        p.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0o600 (Unix)
    except Exception:
        pass  # ignore on platforms without chmod semantics


def _read_index() -> dict:
    if not INDEX_PATH.exists():
        return {}
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_index(idx: dict) -> None:
    tmp = INDEX_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    tmp.replace(INDEX_PATH)


# =====================
# DID key/Doc utilities
# =====================
# multicodec prefix for Ed25519 public key = 0xED 0x01
ED25519_PUB_CODEC_PREFIX = bytes([0xED, 0x01])


def _to_base58btc(b: bytes) -> str:
    return "z" + base58.b58encode(b).decode("utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_did_key_and_doc(label: str | None = None):
    # 1) Generate Ed25519 keypair
    sk = SigningKey.generate()
    pk = sk.verify_key
    pk_bytes = pk.encode(encoder=RawEncoder)  # 32 bytes

    # 2) did:key fingerprint = mb(base58btc(multicodec + pubkey))
    fingerprint_bytes = ED25519_PUB_CODEC_PREFIX + pk_bytes
    fingerprint = _to_base58btc(fingerprint_bytes)

    did = f"did:key:{fingerprint}"
    vm_id = f"{did}#{fingerprint}"

    # 3) DID Document (Multikey format)
    did_document = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "id": did,
        "verificationMethod": [
            {
                "id": vm_id,
                "type": "Multikey",
                "controller": did,
                "publicKeyMultibase": _to_base58btc(pk_bytes),
            }
        ],
        "authentication": [vm_id],
        "assertionMethod": [vm_id],
        "capabilityInvocation": [vm_id],
        "capabilityDelegation": [vm_id],
        "keyAgreement": [],
    }

    # 4) Private key export (server-side only, DO NOT return to clients)
    private_export = {
        "kty": "OKP",
        "crv": "Ed25519",
        "d": sk.encode(encoder=RawEncoder).hex(),   # hex for simplicity
        "x": pk_bytes.hex(),
        "alg": "EdDSA",
    }

    meta = {
        "did": did,
        "fingerprint": fingerprint,
        "label": label,
        "created_at": _now_iso(),
    }
    return did, fingerprint, did_document, private_export, meta


def persist_to_disk(fingerprint: str, doc: dict, private_export: dict, meta: dict):
    # Write DID Document
    did_path = DIDS_DIR / f"{fingerprint}.did.json"
    with did_path.open("w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    # Write private key (server-only)
    key_path = KEYS_DIR / f"{fingerprint}.key.json"
    with key_path.open("w", encoding="utf-8") as f:
        json.dump(private_export, f, ensure_ascii=False, indent=2)
    _chmod_600(key_path)

    # Update index atomically
    with _index_lock:
        idx = _read_index()
        idx[meta["did"]] = {k: meta[k] for k in ("created_at", "label")}
        _write_index(idx)

    return str(did_path), str(key_path)


# =====================
# HTTP Endpoints
# =====================
@did_api.route("/create", methods=['POST'])
def create_did():
    body = request.get_json(silent=True) or {}
    label = body.get("label")

    did, fp, doc, prv, meta = make_did_key_and_doc(label=label)
    did_path, _key_path = persist_to_disk(fp, doc, prv, meta)

    return (
        jsonify({
            "did": did,
            "fingerprint": fp,
            "label": label,
            "stored": {
                "didDocumentPath": did_path,
            },
        }),
        201,
    )


@did_api.get("/dids")
def list_dids():
    """List DIDs known to this server (from index.json)."""
    with _index_lock:
        idx = _read_index()
    # Return sorted by created_at desc
    items = [
        {"did": did, **meta} for did, meta in sorted(
            idx.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True
        )
    ]
    return jsonify({"count": len(items), "items": items})


@did_api.route("resolve/", methods=['POST'])
def resolve_did():
    body = request.get_json(silent=True) or {}
    did_or_fp = body.get("label")

    """Resolve a DID Document from local store.
    Accepts either full DID (did:key:z...) or just the fingerprint (z...).
    """
    did_or_fp = did_or_fp.strip()
    if did_or_fp.startswith("did:key:"):
        fp = did_or_fp.split(":")[-1]
    else:
        fp = did_or_fp
    did_path = DIDS_DIR / f"{fp}.did.json"
    if not did_path.exists():
        abort(404, description="DID not found on server")
    with did_path.open("r", encoding="utf-8") as f:
        doc = json.load(f)
    return jsonify(doc)


@did_api.route("delete/", methods=['POST'])
def delete_did():
    body = request.get_json(silent=True) or {}
    did_or_fp = body.get("label")
    """Delete DID Document and private key from local store."""
    did_or_fp = did_or_fp.strip()
    if did_or_fp.startswith("did:key:"):
        fp = did_or_fp.split(":")[-1]
        did_full = did_or_fp
    else:
        fp = did_or_fp
        did_full = f"did:key:{fp}"

    did_path = DIDS_DIR / f"{fp}.did.json"
    key_path = KEYS_DIR / f"{fp}.key.json"

    removed = {"didDocument": False, "privateKey": False}

    if did_path.exists():
        did_path.unlink()
        removed["didDocument"] = True
    if key_path.exists():
        key_path.unlink()
        removed["privateKey"] = True

    with _index_lock:
        idx = _read_index()
        if did_full in idx:
            del idx[did_full]
            _write_index(idx)

    if not any(removed.values()):
        abort(404, description="Nothing to delete (DID not found)")

    return jsonify({"deleted": removed, "did": did_full})

# --- helpers: DID/키 로딩 ---
def _fp_from_did(did: str) -> str:
    if not did.startswith("did:key:"):
        raise ValueError("Only did:key supported")
    return did.split(":")[-1]

def _load_private_key_by_did(did: str) -> Tuple[Ed25519PrivateKey, str]:
    fp = _fp_from_did(did)
    key_path = KEYS_DIR / f"{fp}.key.json"
    if not key_path.exists():
        raise FileNotFoundError("private key not found on server")
    with key_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # our stored format: hex strings d (private), x (public)
    d_hex = data["d"]
    sk_bytes = bytes.fromhex(d_hex)
    sk = Ed25519PrivateKey.from_private_bytes(sk_bytes)
    return sk, fp

def _load_public_key_from_diddoc(did: str) -> Ed25519PublicKey:
    fp = _fp_from_did(did)
    did_path = DIDS_DIR / f"{fp}.did.json"
    if not did_path.exists():
        raise FileNotFoundError("issuer DID Document not found on server")
    with did_path.open("r", encoding="utf-8") as f:
        doc = json.load(f)
    # We stored verificationMethod[0].publicKeyMultibase == base58btc of raw 32 bytes
    vms = doc.get("verificationMethod", [])
    if not vms:
        raise ValueError("No verificationMethod in DID Document")
    pk_mb = vms[0].get("publicKeyMultibase")
    if not (pk_mb and pk_mb.startswith("z")):
        raise ValueError("Unsupported publicKeyMultibase")
    pk_bytes = base58.b58decode(pk_mb[1:])  # raw 32-byte Ed25519 public key
    return Ed25519PublicKey.from_public_bytes(pk_bytes)

def _jwt_now():  # seconds
    return int(time.time())

# --- VC 발급 (VC-JWT) ---
@did_api.route("/issue-vc", methods=['POST'])
def issue_vc():
    """
    Body:
    {
      "issuer": "did:key:z6Mk...",   # 서버에 저장된 발급자 DID
      "subject": "did:key:z6Hk...",  # 소지자 DID(피발급자)
      "claims": { "name": "Alice", "employeeId": "E-123" },  # credentialSubject
      "ttl": 3600,                   # 초 (기본 1시간)
      "aud": "optional-audience"     # 선택: verifier 식별자(검증때 요구)
    }
    Returns: { "vc_jwt": "<JWT string>" }
    """
    body = request.get_json(silent=True) or {}
    issuer = body.get("issuer")
    subject = body.get("subject")
    cs_claims = body.get("claims", {})
    ttl = int(body.get("ttl", 3600))
    aud = body.get("aud")

    if not issuer or not subject:
        abort(400, description="issuer and subject are required")

    sk, _ = _load_private_key_by_did(issuer)
    now = _jwt_now()
    exp = now + ttl

    # VC-JWT payload (W3C VC-JWT)
    vc = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential"],
        "credentialSubject": cs_claims
    }

    payload = {
        "iss": issuer,
        "sub": subject,
        "nbf": now,
        "iat": now,
        "exp": exp,
        "vc": vc
    }
    if aud:
        payload["aud"] = aud

    # PyJWT는 EdDSA에 cryptography의 Ed25519PrivateKey를 바로 사용 가능
    vc_jwt = jwt.encode(payload, sk, algorithm="EdDSA")
    return jsonify({"vc_jwt": vc_jwt, "exp": exp})

# --- VC 검증 ---
@did_api.route("/verify-vc", methods=["POST"])
def verify_vc():
    """
    Body: { "vc_jwt": "<JWT string>", "aud": "optional-required-audience" }
    Steps:
      1) iss를 추출
      2) 서버 저장 DID Document에서 공개키 추출
      3) EdDSA로 서명/만료/nbf/aud 검증
    Returns: { "valid": true/false, "reason": "...", "payload": {...} }
    """
    body = request.get_json(silent=True) or {}
    token = body.get("vc_jwt")
    aud = body.get("aud")
    if not token:
        abort(400, description="vc_jwt is required")

    ok, data = verify_vc_token(token, aud=aud)
    if ok:
        return jsonify({"valid": True, "payload": data})
    return jsonify({"valid": False, "reason": data}), 400

# --- VP 생성 (VP-JWT with embedded VC-JWTs) ---
@did_api.route("/present-vp", methods=['POST'])
def present_vp():
    """
    Body:
    {
      "holder": "did:key:z6Hk...",     # VP 서명 주체
      "vc_jwts": ["<...>"],            # 포함할 VC-JWT 배열
      "aud": "verifier-id-or-url",     # 검증자가 기대하는 audience
      "ttl": 300                       # 발표 토큰 TTL(초)
    }
    Returns: { "vp_jwt": "<JWT string>" }
    """
    body = request.get_json(silent=True) or {}
    holder = body.get("holder")
    vc_jwts = body.get("vc_jwts", [])
    aud = body.get("aud")
    ttl = int(body.get("ttl", 300))

    if not holder or not vc_jwts or not aud:
        abort(400, description="holder, vc_jwts, aud are required")

    sk, _ = _load_private_key_by_did(holder)
    now = _jwt_now()
    exp = now + ttl

    vp = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiablePresentation"],
        "verifiableCredential": vc_jwts
    }
    payload = {
        "iss": holder,
        "aud": aud,
        "nbf": now,
        "iat": now,
        "exp": exp,
        "vp": vp
    }
    vp_jwt = jwt.encode(payload, sk, algorithm="EdDSA")
    return jsonify({"vp_jwt": vp_jwt, "exp": exp})

# --- VP 검증 ---
@did_api.route("/verify-vp", methods=["POST"])
def verify_vp():
    """
    Body: { "vp_jwt": "<JWT string>", "aud": "expected-aud" }
    1) holder DID 문서의 공개키로 VP-JWT 서명/만료/aud 검증
    2) vp.verifiableCredential[]의 각 VC-JWT는 /verify-vc 로 개별 검증
    Returns: { valid, reason?, holder, vcs: [{valid, reason?, iss, sub}], payload }
    """
    body = request.get_json(silent=True) or {}
    token = body.get("vp_jwt")
    expected_aud = body.get("aud")
    if not token or not expected_aud:
        abort(400, description="vp_jwt and aud are required")

    # holder 파악
    try:
        unverified = jwt.decode(token, options={"verify_signature": False})
        holder = unverified.get("iss")
        if not holder:
            raise ValueError("No iss in VP")
    except Exception as e:
        return jsonify({"valid": False, "reason": f"malformed token: {e}"}), 400

    # VP 서명 검증
    try:
        pk = _load_public_key_from_diddoc(holder)
        payload = jwt.decode(
            token, pk, algorithms=["EdDSA"],
            options={"require": ["iss", "aud", "exp", "nbf", "iat"]},
            audience=expected_aud,
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "reason": "expired"}), 400
    except jwt.InvalidAudienceError:
        return jsonify({"valid": False, "reason": "audience mismatch"}), 400
    except Exception as e:
        return jsonify({"valid": False, "reason": str(e)}), 400

    # 포함된 VC-JWT들 개별 검증 (aud는 일반적으로 None이거나 verifier 정책에 맞게)
    vcs = []
    for vc_jwt in payload.get("vp", {}).get("verifiableCredential", []):
        ok, data = verify_vc_token(vc_jwt, aud=None)
        if ok:
            vcs.append({"valid": True, "iss": data.get("iss"), "sub": data.get("sub")})
        else:
            vcs.append({"valid": False, "reason": data})

    all_ok = all(v.get("valid") for v in vcs)
    return jsonify({"valid": all_ok, "holder": holder, "vcs": vcs, "payload": payload})
