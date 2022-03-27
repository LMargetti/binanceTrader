# imports
from binance.client import Client
from decouple import config


def main():
    test_key = config('test_key')
    test_secret = config('test_secret')

    # initialise the client
    client = Client(test_key, test_secret)
    client.API_URL = 'https://testnet.binance.vision/api'
    print(client.get_asset_balance(asset="BTC"))


if __name__ == "__main__":
    main()
