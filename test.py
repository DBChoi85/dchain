import requests
from myapp import utils

url = utils.BASE_URL + '/token/create'
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
response = requests.post(url, json=data)
print(response.json())