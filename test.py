from decouple import config

api_key = config('binance_key')
api_secret = config('binance_secret')

print(api_key)
print(api_secret)