import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

# set the Binance API key and secret
binance_api_key = os.getenv('API_KEY')
binance_api_secret = os.getenv('API_SECRET')

# set the Line API access token
line_token = os.getenv('LINE_TOKEN')

# set the Bollinger Band parameters
bb_period = 20
bb_stddev = 2

# create a Binance client
client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


