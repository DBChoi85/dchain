import requests
from myapp import utils

url = "http://localhost:5000"+'/token/refresh_balance'
# token_name = request.args.get("token_name")
# token_symbol = request.args.get("token_symbol")
# supply = request.args.get('supply')
token_name = 'test'
token_symbol = "TEST"
supply = 100
data = {
    "token" : utils.API_TOKEN,
    "chain" : utils.CHAIN_NAME,
    "owner_addr" : utils.OWNER_ADDR,
    "owner_pkey" : utils.OWNER_PRIVATE,
    "token_name" : token_name,
    "token_symbol" : token_symbol,
    "decimals" : 9,
    "supply" : supply,       
}

token_data = {
        "token" : utils.API_TOKEN,
        "chain" : utils.CHAIN_NAME,
        "contract_address" : '0x4a1dD7273b37669e6A926e5F9C77aDFa9fe1E826fca',
        "sender" : utils.OWNER_ADDR,
        "sender_private_key" : utils.OWNER_PRIVATE,
        "receiver" : '0x680F2FbD587ba8099D39f2930557EFf5B1382BB0fca',
        "amount" : 50
    }

addr = {'address': '0x726E3815F33677c6DF46A6B24E3357daaA93ABC3fca'}
# response = requests.post(url, json=token_data)
# print(token_data)
# print(response.json())

response = requests.post(url)
print(response.json())