import requests
from myapp import utils

url = "http://localhost:5000"+'/acc/get_private_key'
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

addr = {'address': '0x726E3815F33677c6DF46A6B24E3357daaA93ABC3fca'}
response = requests.post(url, json=addr)
print(response.text)