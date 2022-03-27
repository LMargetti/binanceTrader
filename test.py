# imports
from binance.client import Client
from decouple import config
from time import sleep
from binance import ThreadedWebsocketManager


def btc_trade_history(msg):
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
        btc_price['error'] = False
    else:
        btc_price['error'] = True


test_key = config('test_key')
test_secret = config('test_secret')

# initialise the client
client = Client(test_key, test_secret)
client.API_URL = 'https://testnet.binance.vision/api'
print(client.get_asset_balance(asset="BTC"))

btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
print(btc_price)


bsm = ThreadedWebsocketManager()

bsm.start_symbol_ticker_socket(callback=btc_trade_history(),
                               symbol='BTCUSDT')

