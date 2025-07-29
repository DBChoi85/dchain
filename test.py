import requests
from myapp import utils

base_url = "http://localhost:5000/token/"
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
        "contract_address" : '0x6E830ad7eE16877f127A06d5682C11E0B60f7d19fca',
        "sender" : utils.OWNER_ADDR,
        "sender_private_key" : utils.OWNER_PRIVATE,
        "receiver" : '0x680F2FbD587ba8099D39f2930557EFf5B1382BB0fca',
        "amount" : 10
    }

addr = {'address': '0x726E3815F33677c6DF46A6B24E3357daaA93ABC3fca'}

# create_token = requests.post(base_url + 'create', json=data)
# print(create_token.json())

# transfer_token = requests.post(base_url + 'transfer', json=token_data)
# print(transfer_token.json())

# r_data = {
#         "contract_address" : '0x6E830ad7eE16877f127A06d5682C11E0B60f7d19fca',
# }

# refresh_balance = requests.post(base_url+'refresh_balance', json=r_data)
# print(refresh_balance.json())

# retrieve_data = {
#     "contract_address" : '0x6E830ad7eE16877f127A06d5682C11E0B60f7d19fca',
#     "holder" : '0x680F2FbD587ba8099D39f2930557EFf5B1382BB0fca',
#     "receiver" : utils.OWNER_ADDR,
#     "amount" : 100
# }

# retrieve_token = requests.post(base_url+'retrieve', json=retrieve_data)
# print(retrieve_token.json())


# response = requests.post(url, json=token_data)
# print(token_data)
# print(response.json())

# response = requests.post(url)
# print(response.json())