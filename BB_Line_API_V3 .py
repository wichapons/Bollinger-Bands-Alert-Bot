import talib
import numpy as np
import requests
import json
import time
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

# set the Binance API key and secret
binance_api_key = os.getenv('API_KEY')
binance_api_secret = os.getenv('API_SECRET')

# set the Line API access token
line_token = os.getenv('LINE_TOKEN')

# set the symbol and timeframe
symbol = "BNBUSDT"
timeframe = "1h"

# set the Bollinger Band parameters
bb_period = 20
bb_stddev = 2

# create a Binance client
client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

# function to send a Line API alert
def send_line_alert(line_token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + line_token}
    payload = {"message": message}
    r = requests.post(url, headers=headers, data=payload)

#send_line_alert(line_token,'hello world, Phuwit')
i=0

while True:
    try:

        candle_data = client.futures_klines(symbol=symbol, interval=timeframe, limit=bb_period+1)
        low_prices = np.array([float(x[4]) for x in candle_data])
        upper_bb, middle_bb, lower_bb = talib.BBANDS(low_prices, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)

        # check if the Bollinger Bands are contracting
        if upper_bb[-1] - lower_bb[-1] < middle_bb[-1]:
            # check if the current candle hits the upper bound Bollinger Band line
            if low_prices[-1] > middle_bb[-1]:
                # send the alert via Line API
                send_line_alert(line_token, f"{symbol}, price: {low_prices[-1]}, candle tf 15m hit upper bound Bollinger Band line on 1 hr")

            # check if the current candle hits the lower bound Bollinger Band line
            if low_prices[-1] < lower_bb[-1]:
                # send the alert via Line API
                send_line_alert(line_token, f"{symbol}, price: {low_prices[-1]}, candle tf 15m hit lower bound Bollinger Band line on tf 1hr")
    
        # wait for the next candle
        time.sleep(60*15) # wait for 15 minutes
        

    except:
        # handle any errors
        print("An error occurred.")
        time.sleep(60) # wait for 1 minute before retrying




  
