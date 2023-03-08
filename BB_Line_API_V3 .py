import time
from dotenv import load_dotenv
from config import symbol,timeframe
from line_alert import send_line_alert
from wait_duration import waitTime
from candle_data import candleData
load_dotenv()

# set up initial timer value and flag variables
last_alert_time, upper_alert_triggered, upper_middle_alert_triggered, lower_middle_alert_triggered, lower_alert_triggered,bot_status = 0, False, False, False, False,0

while True:
    try:
        wait_time = waitTime()  #get the value from def waitTime

        if bot_status == 0:
            send_line_alert(f'bot had been restarted successfully, next alert will begin in {wait_time/60} minutes ')
            bot_status = 1  
                 
        print(f'next notify in {wait_time/60} minutes')
        time.sleep(wait_time)
        # update data
        upper_bb, middle_bb, lower_bb,low_prices,high_prices = candleData()

        # check if the Bollinger Bands are contracting
        if upper_bb[-1] - lower_bb[-1] < middle_bb[-1]:

            if high_prices[-1] > middle_bb[-1]:
                if not upper_middle_alert_triggered:
                    send_line_alert(f"{symbol}, Highest candle price: {high_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    upper_middle_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                upper_middle_alert_triggered = False
            
            if low_prices[-1] < middle_bb[-1]:
                if not lower_middle_alert_triggered:
                    send_line_alert( f"{symbol}, Lowest candle price: {low_prices[-1]}, timeframe: {timeframe}, hit middle BB")
                    lower_middle_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                lower_middle_alert_triggered = False

            if low_prices[-1] < lower_bb[-1]:               
                if not lower_alert_triggered:
                    send_line_alert( f"{symbol}, Lowest price: {low_prices[-1]}, timeframe: {timeframe}, hit lower BB.")
                    lower_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                lower_alert_triggered = False

            if high_prices[-1] > upper_bb[-1]:                
                if not upper_alert_triggered:                  
                    send_line_alert( f"{symbol}, Highest price: {high_prices[-1]}, timeframe: {timeframe}, hit upper BB.")
                    upper_alert_triggered = True
            else:
                # reset the upper alert triggered flag
                upper_alert_triggered = False

    except:
        # handle any errors
        print("An error occurred.")
        send_line_alert("An error occurred. Retrying in 1 minute")
        time.sleep(60) # wait for 1 minute before retrying



  