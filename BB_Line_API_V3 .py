import talib
import numpy as np
import time
from dotenv import load_dotenv
from config import *
from line_alert import send_line_alert
from wait_duration import waitTime
from candle_data import candleData
load_dotenv()

# set up initial timer value and flag variables
last_alert_time = 0
upper_alert_triggered = False
upper_middle_alert_triggered = False
lower_middle_alert_triggered = False
lower_alert_triggered = False

while True:
    try:
        wait_time = waitTime()  #get the value from def waitTime
        print(f'next notify in {wait_time/60} minutes')
        time.sleep(wait_time)

        # update data
        upper_bb, middle_bb, lower_bb,low_prices,high_prices = candleData()

        # check if the Bollinger Bands are contracting
        if upper_bb[-1] - lower_bb[-1] < middle_bb[-1]:

            # check if the current highest price candle hits the middle Bollinger Band line
            if high_prices[-1] > middle_bb[-1]:
                # check if the upper alert has not been triggered yet
                if not upper_middle_alert_triggered:
                    send_line_alert(f"{symbol}, High candle price: {high_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    # set the upper alert triggered flag
                    upper_middle_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                upper_middle_alert_triggered = False
            

            # check if the current lowest price candle hits the middle Bollinger Band line
            if low_prices[-1] < middle_bb[-1]:
                # check if the upper alert has not been triggered yet
                if not lower_middle_alert_triggered:
                    send_line_alert( f"{symbol}, Low candle price: {low_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    # set the upper alert triggered flag
                    lower_middle_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                lower_middle_alert_triggered = False

            # check if the current candle hits the lower bound Bollinger Band line
            if low_prices[-1] < lower_bb[-1]:
                
                if not lower_alert_triggered:
                    send_line_alert( f"{symbol}, Lowest price: {low_prices[-1]}, timeframe: {timeframe}, hit lower BB.")
                    # set the upper alert triggered flag
                    lower_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                lower_alert_triggered = False

             # check if the current candle hits the upper bound Bollinger Band line
            if high_prices[-1] > upper_bb[-1]:
                
                if not upper_alert_triggered:                  
                    send_line_alert( f"{symbol}, Lowest price: {high_prices[-1]}, timeframe: {timeframe}, hit lower BB.")
                    # set the upper alert triggered flag
                    upper_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                upper_alert_triggered = False



    except:
        # handle any errors
        print("An error occurred.")
        send_line_alert("An error occurred. Retrying in 1 minute")
        time.sleep(60) # wait for 1 minute before retrying



  