import talib
from default import *
import numpy as np

# set the symbol and timeframe
symbol = "BNBUSDT"
timeframe = "1h"

# update data
candle_data = client.futures_klines(symbol=symbol, interval=timeframe, limit=bb_period+1)
low_prices = np.array([float(x[4]) for x in candle_data])
high_prices = np.array([float(x[2]) for x in candle_data])
upper_bb, middle_bb, lower_bb = talib.BBANDS(low_prices, timeperiod=bb_period, nbdevup=bb_stddev, nbdevdn=bb_stddev, matype=0)
