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
symbol = "RUNEUSDT"
timeframe = "15m"

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
        # get the candle data from Binance  **15m**
        candle_data = client.futures_klines(symbol=symbol, interval=timeframe, limit=bb_period+1)
        candle_data_tf_5m = client.futures_klines(symbol=symbol, interval="5m", limit=bb_period+1)
        candle_data_tf_1m = client.futures_klines(symbol=symbol, interval="1m", limit=bb_period+1)

        # extract the lowest prices from the candle data
        low_prices = np.array([float(x[4]) for x in candle_data])
        low_prices_tf_5m = np.array([float(x[4]) for x in candle_data_tf_5m])
        low_prices_tf_1m = np.array([float(x[4]) for x in candle_data_tf_1m])
        
        #lowest_prices = []

        # group the low prices by time frame
        #for i in range(0, len(low_prices), bb_period):
        #    lowest_prices.append(min(low_prices[i:i+bb_period]))

        # convert the lowest prices to a numpy array
        #lowest_prices = np.array(lowest_prices)


        # calculate the Bollinger Bands
        upper_bb, middle_bb, lower_bb = talib.BBANDS(low_prices, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)

        # extract the close prices from the candle data
        #close_prices = np.array([float(x[4]) for x in candle_data])
        
        # calculate the Bollinger Bands
        #upper_bb, middle_bb, lower_bb = talib.BBANDS(close_prices, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)


        # check if the Bollinger Bands are contracting
        if upper_bb[-1] - lower_bb[-1] < middle_bb[-1]:
            # check if the current candle hits the upper bound Bollinger Band line

            if low_prices[-1] > upper_bb[-1]:
                # send the alert via Line API
                send_line_alert(line_token, f"{symbol}, price: {low_prices[-1]}, candle tf 15m hit upper bound Bollinger Band line on tf 15 m")

            # check if the current candle hits the lower bound Bollinger Band line
            if low_prices[-1] < lower_bb[-1]:
                # send the alert via Line API
                send_line_alert(line_token, f"{symbol}, price: {low_prices[-1]}, candle tf 15m hit lower bound Bollinger Band line on tf 15 m")
    
        # wait for the next candle
        i=i+1
        print(i)
        print(candle_data)
        print(low_prices)
        print(low_prices_tf_1m)
        print(upper_bb)
        print(upper_bb[-1])
        print(lower_bb)
        print(lower_bb[-1])
        print("start monitoring BB")
        time.sleep(60*15) # wait for 1 minutes

    except:
        # handle any errors
        print("An error occurred.")
        time.sleep(60) # wait for 1 minute before retrying




  
