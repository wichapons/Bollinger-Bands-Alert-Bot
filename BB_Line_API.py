import os
import time
import requests
import json
import numpy as np
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
load_dotenv()

api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

line_token = os.getenv('LINE_TOKEN')

symbol = 'RUNEUSDT'
interval = '15m'
window = 20
multiplier = 2

candles = client.futures_historical_klines(
    start_str=None,
    symbol=symbol,
    interval=interval,
    limit=window
)

close = np.array([float(candle[4]) for candle in candles])

sma = np.mean(close)
std = np.std(close)
upper_bb = sma + multiplier * std
lower_bb = sma - multiplier * std

def send_line_notification(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_token}'}
    data = {
        'message': message}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print('Failed to send LINE notification')

send_line_notification('hello world')

i = 0

while True:
    candle = client.futures_klines(symbol=symbol, interval=interval, limit=1)[0]
    close = float(candle[4])
    sma = np.mean(close)
    std = np.std(close)
    upper_bb = sma + multiplier * std
    lower_bb = sma - multiplier * std

    print(i)
    print(candles)
    i=i+1
    if std / sma < 0.05:
        if close > upper_bb:
            message = f'{symbol} {interval} Upper BB Alert: {close}'
            send_line_notification(message)
            print(message)
        elif close < lower_bb:
            message = f'{symbol} {interval} Lower BB Alert: {close}'
            send_line_notification(message)
            print(message)

    time.sleep(60*15)
