from flask import Blueprint, request, jsonify
from myapp.utils import BASE_URL, API_TOKEN, CHAIN_NAME, HEADERS
import requests
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import set_acc_list
import get_acc_list

acc_api = Blueprint('acc', __name__)
set_acc_db = set_acc_list.Acc_List()
get_acc_db = get_acc_list.Acc_List()


@acc_api.route('/create', methods=['POST'])
def create_acc():
    url = BASE_URL + '/com/acc_create'
    data = {
        "token":API_TOKEN,
        "chain":CHAIN_NAME
    }
    response = requests.post(url,json=data)
    if response.status_code == 200:
        response_data = response.json()
        acc_data = response_data['data']['key_pair']
        addr = acc_data['address']
        set_acc_db.save_private_key(addr, acc_data['privatekey'])
        set_acc_db.save_public_key(addr, acc_data['publickey'])
        return addr
    else:
        return response

@acc_api.route('/get_list', methods=['GET'])
def get_acc_list():
    acc_list = get_acc_db.all_list()
    return jsonify(acc_list)

@acc_api.route('/get_public_key', methods=['GET'])
def get_public_key():
    addr = request.args.get("address")
    public_key = get_acc_db.get_public_key(addr)
    return jsonify(public_key)

@acc_api.route('/get_private_key', methods=['GET'])
def get_private_key():
    addr = request.args.get("address")
    private_key = get_acc_db.get_private_key(addr)
    return jsonify(private_key)



if __name__ == "__main__":
    r = create_acc()
    print(get_acc_db.get_public_key(r))