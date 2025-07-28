import requests
from myapp import utils

url = "http://localhost:5000"+'/acc/get_public_key'
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

addr = {'address': '0x5fD5111165c6E160dE4BFdf8440c1B7Fc92048b1fca'}
response = requests.get(url, params=addr)
print(response.json())