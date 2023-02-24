import time
from line_alert import send_line_alert
from default import *
from wait_duration import*
from candle_data import *

while True:
    try:
        # wait until next quarter hour
        time.sleep(wait_time)

        # check if the Bollinger Bands are contracting
        if upper_bb[-1] - lower_bb[-1] < middle_bb[-1]:

            # check if the current highest price candle hits the middle Bollinger Band line
            if high_prices[-1] > middle_bb[-1]:
                # check if the upper alert has not been triggered yet
                if not upper_middle_alert_triggered:
                    # send the alert via Line API
                    send_line_alert(line_token, f"{symbol}, High candle price: {high_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    # set the upper alert triggered flag
                    upper_middle_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                upper_middle_alert_triggered = False
            
            # check if the current lowest price candle hits the middle Bollinger Band line
            if low_prices[-1] < middle_bb[-1]:
                # check if the upper alert has not been triggered yet
                if not lower_middle_alert_triggered:
                    # send the alert via Line API
                    send_line_alert(line_token, f"{symbol}, Low candle price: {low_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    # set the upper alert triggered flag
                    lower_middle_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                lower_middle_alert_triggered = False

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

             # check if the current candle hits the upper bound Bollinger Band line
            if high_prices[-1] > upper_bb[-1]:
                
                if not upper_alert_triggered:
                    # send the alert via Line API
                    send_line_alert(line_token, f"{symbol}, Lowest price: {high_prices[-1]}, timeframe: {timeframe}, hit higher BB.")
                    # set the upper alert triggered flag
                    upper_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                upper_alert_triggered = False
    except:
        # handle any errors
        print("An error occurred.")
        send_line_alert(line_token,"An error occurred. Retrying in 1 minute")
        time.sleep(60) # wait for 1 minute before retrying




  
