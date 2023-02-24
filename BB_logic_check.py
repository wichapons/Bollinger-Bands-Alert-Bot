from line_alert import * 
from candle_data import *

def highCandleHitMidBB ():
    # send the alert via Line API
    send_line_alert(line_token, f"{symbol}, High candle price: {high_prices[-1]}, timeframe: {timeframe}, hit middle BB")
    # set the upper alert triggered flag
    upper_middle_alert_triggered = True