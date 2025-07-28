from flask import Blueprint, request, jsonify
from myapp.utils import BASE_URL, API_TOKEN, CHAIN_NAME, HEADERS, OWNER_ADDR, OWNER_PRIVATE
import requests

token_api = Blueprint('token', __name__)

@token_api.route('/create', methods=['POST','GET'])
def create_token():
    url = BASE_URL + '/token/create'
    # token_name = request.args.get("token_name")
    # token_symbol = request.args.get("token_symbol")
    # supply = request.args.get('supply')
    token_name = 'test'
    token_symbol = "TEST"
    supply = 100
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
    if response.status_code == 200:
        response_data = response.json()



if __name__ is "__main__":
    r = create_token()
    print(r)