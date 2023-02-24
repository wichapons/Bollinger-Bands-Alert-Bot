import talib
import numpy as np
import requests
import json
import time
from binance.client import Client
from dotenv import load_dotenv
import os
import datetime
load_dotenv()

# set up initial timer value and flag variables
last_alert_time = 0
lower_alert_triggered = False
middle_alert_triggered = False

# set up initial timer value and flag variables
last_alert_time = 0
lower_alert_triggered = False
middle_alert_triggered = False

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

while True:
    try:
        # get current minute value
        current_time = datetime.datetime.now()
        current_minute = current_time.minute

        # calculate time until next hour
        if current_minute < 60:
            wait_time = ((60 - current_minute) * 60 - current_time.second)+5  #add 5 sec delay prevent .json data is not ready in time
        print(f'next notify in {wait_time/60} minutes')
        # wait until next quarter hour
        time.sleep(wait_time)

        # update data
        candle_data = client.futures_klines(symbol=symbol, interval=timeframe, limit=bb_period+1)
        low_prices = np.array([float(x[4]) for x in candle_data])
        high_prices = np.array([float(x[2]) for x in candle_data])
        high_prices = np.array([float(x[2]) for x in candle_data])
        upper_bb, middle_bb, lower_bb = talib.BBANDS(low_prices, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)

        # check if the Bollinger Bands are contracting
        if upper_bb[-1] - lower_bb[-1] < middle_bb[-1]:
            # check if the current candle hits the upper middle Bollinger Band line
            if high_prices[-1] > middle_bb[-1]:
                # check if the upper alert has not been triggered yet
                if not middle_alert_triggered:
                    # send the alert via Line API
                    send_line_alert(line_token, f"{symbol}, High candle price: {high_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    # set the upper alert triggered flag
                    middle_alert_triggered = True
                else:
                    # reset the upper alert triggered flag
                    middle_alert_triggered = False

            # check if the current candle hits the lower bound Bollinger Band line
            if low_prices[-1] < lower_bb[-1]:
                
                if not lower_alert_triggered:
                    # send the alert via Line API
                    send_line_alert(line_token, f"{symbol}, Lowest price: {low_prices[-1]}, timeframe: {timeframe}, hit lower BB.")
                    # set the upper alert triggered flag
                    lower_alert_triggered = True
                else:
                    # reset the upper alert triggered flag
                    lower_alert_triggered = False
    
    except:
        # handle any errors
        print("An error occurred.")
        send_line_alert(line_token,"An error occurred. Retrying in 1 minute")
        time.sleep(60) # wait for 1 minute before retrying

  