import talib
import numpy as np
from config import *

def candleData():
    # update data
    candle_data = client.futures_klines(symbol=symbol, interval=timeframe, limit=bb_period+1)
    low_prices = np.array([float(x[4]) for x in candle_data])
    high_prices = np.array([float(x[2]) for x in candle_data])
    upper_bb, middle_bb, lower_bb = talib.BBANDS(low_prices, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)
    return upper_bb, middle_bb, lower_bb,low_prices,high_prices
