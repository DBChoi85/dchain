from flask import Blueprint, request, jsonify
from myapp.utils import BASE_URL, API_TOKEN, CHAIN_NAME, HEADERS, OWNER_ADDR, OWNER_PRIVATE
import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import set_token_list
import set_acc_balance
import get_acc_balance
import get_acc_list
import set_receipt_list

token_api = Blueprint('token', __name__)
set_token_db = set_token_list.Toekn_List()
set_balance_db = set_acc_balance.Balance_List()
get_balance_db = get_acc_balance.Balance_List()
get_acc_db = get_acc_list.Acc_List()
set_receipt_db = set_receipt_list.Receipt_List()

@token_api.route('/create', methods=['POST'])
def create_token():
    url = BASE_URL + '/token/create'
    input_data = request.get_json()
    token_name = input_data['token_name']
    token_symbol = input_data['token_symbol']
    supply = input_data['supply']
    data = {
        "token" : API_TOKEN,
        "chain" : CHAIN_NAME,
        "owner_addr" : OWNER_ADDR,
        "owner_pkey" : OWNER_PRIVATE,
        "token_name" : token_name,
        "token_symbol" : token_symbol,
        "decimals" : 9,
        "supply" : supply,       
    }
    response = requests.post(url,json=data)
    # print(response.json())
    if response.status_code == 200:
        response_data = response.json()
        contract_addr = response_data['data']['contract']['data']['address']
        issued = response_data['data']['contract']['issued']
        set_token_db.set_token(addr=OWNER_ADDR, token_name=token_name, token_symbol=token_symbol, contract_addr=contract_addr, issued=issued, supply=supply, meta_data=response_data)
        set_token_db.commit()
        set_balance_db.connect(str(contract_addr))
        set_balance_db.set_balance(OWNER_ADDR, supply)
        set_balance_db.commit()
        retrun_data = {"contract address": contract_addr}
        return jsonify(retrun_data)
    else:
        return response
    
@token_api.route('/transfer', methods=['POST'])
def token_transfer():
    url = BASE_URL + '/token/transfer'
    input_data = request.get_json()
    contract_address = input_data['contract_address']
    sender = input_data['sender']
    sender_private_key = input_data['sender_private_key']
    receiver = input_data['receiver']
    amount = input_data['amount']
    data = {
        "token" : API_TOKEN,
        "chain" : CHAIN_NAME,
        "cont_addr" : contract_address,
        "sender" : sender,
        "sender_pkey" : sender_private_key,
        "receiver" : receiver,
        "amount" : amount
    }
    response = requests.post(url,json=data)
    set_balance_db.connect(str(contract_address))
    get_balance_db.connect(str(contract_address))

    if response.status_code == 200:
        response_data = response.json()
        receipt_sender = response_data['data']['receipt']['operation']['fact']['sender']
        receipt_receiver = response_data['data']['receipt']['operation']['fact']['reciver']
        receipt_amount = response_data['data']['receipt']['operation']['fact']['amount']
        set_balance_db.decrease_balance(receipt_sender, receipt_amount)
        set_balance_db.increase_balance(receipt_receiver, receipt_amount)
        set_balance_db.commit()
        receipt_issued = response_data['data']['issued']
        set_receipt_db.set_receipt(contract_address, receipt_issued, receipt_sender, receipt_receiver, receipt_amount, response_data)
        set_receipt_db.commit()
        return jsonify(response_data)
    else:
        return response.json()
    
@token_api.route('/balance_list', methods=['POST'])
def token_balance():
    input_data = request.get_json()
    contract_address = input_data['contract_address']
    get_balance_db.connect(str(contract_address))
    balance_list = get_balance_db.all_list()
    return jsonify(balance_list)

@token_api.route('/retrieve', methods=['POST'])
def token_retrieve():
    input_data = request.get_json()
    contract_address = input_data['contract_address']
    holder = input_data['holder']
    receiver = input_data['receiver']
    amount = input_data['amount']
    holder_pkey = get_acc_db.get_private_key(holder)
    print("target pkey : {}".format(holder_pkey))

    approve_data = {
        "token" : API_TOKEN,
        "chain" : CHAIN_NAME,
        "cont_addr" : contract_address,
        "holder" : holder,
        "holder_pkey" : holder_pkey,
        "approved" : receiver,
        "amount" : amount
    }
    approve_url = BASE_URL + '/token/approve'
    response_approve = requests.post(approve_url, json=approve_data)
    if response_approve.status_code == 200:
        print("권한 설정 완료")
    else:
        print("권한 설정 실패 : {}".format(response_approve))

    transfer_from_url = BASE_URL + '/token/transfer_from'
    transfer_data = {
        "token" : API_TOKEN,
        "chain" : CHAIN_NAME,
        "cont_addr" : contract_address,
        "sender" : OWNER_ADDR,
        "sender_pkey" : OWNER_PRIVATE,
        "holder" : holder,
        "receiver" : OWNER_ADDR,
        "amount" : amount
    }

    transfer_from_response = requests.post(transfer_from_url, json=transfer_data)
    if transfer_from_response.status_code == 200:
        return transfer_from_response.json()
    else:
        return transfer_from_response.json()
    

@token_api.route('/refresh_balance', methods=['POST'])
def refresh_balance():
    balance_url = BASE_URL + 'token/balance'
    cont_addr = request.get_json['contract_address']
    set_balance_db.connect(cont_addr)
    acc_list = get_acc_db.all_list()
    for addr in acc_list:
        balance_data = {
            "token" : API_TOKEN,
            "chain" : CHAIN_NAME,
            "cont_addr" : cont_addr,
            "addr" : addr
         }
        response = requests.post(balance_url, json=balance_data)
        balance = response.json()['data']['balance']
        set_balance_db.set_balance(addr, balance=balance)
    
    set_balance_db.commit()
    get_balance_db.connect(cont_addr)
    all_list = get_balance_db.all_list()
    return jsonify(all_list)



if __name__ == "__main__":
    r = create_token()
    print(r)