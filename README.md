# dchain

## 설치 방법
python 3.11 이상 필요  
방화벽에서 접속 port 개방 필요

1. git clone
```
git clone https://github.com/DBChoi85/dchain.git
```
or
```
gh repo clone dbchoi85/dchain
```
2. Dependency install
```
pip install -r requirements.txt
```

## 서비스 환경 설정
접속 port 변경 시 run.py 수정
```
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000, debug=True)
```
host = '0.0.0.0' -> 모든 네트워크 인터페이스, 고정 IP로 설정을 원할 시 해당 IP로 변경  
port = 5000 -> 접속 port, 변경 필요시 해당 port 입력

## utils.py 설정
https://www.daegu.go.kr/daeguchain/baas/setting/key

위 주소에서 아래 변수들 정보를 찾아 utils.py에 업데이트 필요  
API_TOKEN 
<img width="790" height="352" alt="image" src="https://github.com/user-attachments/assets/67e6863b-aff9-4715-8c1e-15c11a51fbae" />

아래 정보는 account를 생성하여 업데이트  
OWNER_ADDR  
OWNER_PRIVATE

토큰 발행 권한을 위해 fauset 받기
faucet API 호출 권한 관련
토큰 발급을 위해 faucet API를 호출하였으나,
"해당 API 호출 권한이 없습니다. (akey)"라는 메시지가 반환되고 있습니다.
해당 문제 해결법에 관해 문의드립니다.
=> API 호출권한 부여를 위해 사용 하시는분들의 BaaS 이메일 계정과 API토큰(또는 App Key) 회신 주시면 등록 후 안내 드리겠습니다.
=> 박우진 <wjpark@rootlab.xyz>

## 서비스 실행 방법
```
python run.py
```



## 각종 DB 및 DID 생성 위치.
