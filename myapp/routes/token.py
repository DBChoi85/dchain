from flask import Blueprint, request, jsonify
from myapp.utils import BASE_URL, API_TOKEN, CHAIN_NAME, HEADERS, OWNER_ADDR
import requests

token_api = Blueprint('token', __name__)

@token_api.route('/create', methods=['GET'])
def create_token():
    url = BASE_URL + '/token/create'
    data = {
        "token" : API_TOKEN,
        "chain" : CHAIN_NAME,
        "owner_addr" : OWNER_ADDR,
        
    }