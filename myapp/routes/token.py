from flask import Blueprint, request, jsonify
from myapp.utils import BASE_URL, API_TOKEN, CHAIN_NAME, HEADERS, OWNER_ADDR, OWNER_PRIVATE
import requests
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import set_token_list
import set_acc_balance
import get_acc_balance

token_api = Blueprint('token', __name__)
set_token_db = set_token_list.Toekn_List()
set_balance_db = set_acc_balance.Balance_List()
get_balance_db = get_acc_balance.Balance_List()

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
        retrun_data = {"contract address": contract_addr}
        return jsonify(retrun_data)
    else:
        return response
    
@token_api.route('/transfer', methods=['POST'])
def token_transfer():
    url = BASE_URL + '/token/create'
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
    if response.status_code == 200:
        check_balance = get_balance_db.get_balance(receiver)
        if check_balance is False:
            set_balance_db.set_balance(receiver, amount)
        else:
            balance = get_balance_db.get_balance(receiver)
            balance += amount
            set_balance_db.update_balance(receiver, balance=balance)

        response_data = response.json()

if __name__ == "__main__":
    r = create_token()
    print(r)