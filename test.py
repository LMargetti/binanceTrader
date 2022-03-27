import timeit

my_setup = '''
from binance.client import Client
from decouple import config
'''

my_code = '''
test_key = config('test_key')
test_secret = config('test_secret')

client = Client(test_key, test_secret)
client.API_URL = 'https://testnet.binance.vision/api'
# print(client.get_asset_balance(asset="BTC"))
'''

print(timeit.timeit(stmt=my_code,
                    setup=my_setup,
                    number=100))
