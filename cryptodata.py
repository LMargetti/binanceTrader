# imports
from binance.client import Client

import asyncio
import os

api_key = os.environ.get('binance_key')
api_secret = os.environ.get('binance_secret')

print(api_key)
print(api_secret)

# async functions
# async def main():
#
#     # initialise the client
#     client = await AsyncClient.create(api_key=api_key,
#                                       api_secret=api_secret)
#
# if __name__ == "__main__":
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
