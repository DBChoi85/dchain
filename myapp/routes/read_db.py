from flask import Blueprint, request, jsonify
from myapp.utils import BASE_URL, API_TOKEN, CHAIN_NAME, HEADERS, OWNER_ADDR, OWNER_PRIVATE
import requests
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import get_receipt_list


db_api = Blueprint('read_db', __name__)
db = get_receipt_list.Read_MeataData()


@db_api.route('/get_md', methods=['POST'])
def get_md():
    input_data = request.get_json()
    cont_addr = input_data['contract_address']
    db.connect(cont_addr)
    response_data = db.get_meta_data('1')
    return jsonify(response_data)


#0xeB9743D10Af108BabED9c8480D0bEccB6b916D7Dfca