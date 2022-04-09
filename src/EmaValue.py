import ccxt
import pandas as pd
from talib import EMA

def getEMA(coin, timeFrame, timePeriod):
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        },
    })

    ohlc = exchange.fetch_ohlcv(coin, timeframe=timeFrame)
    df = pd.DataFrame(ohlc, columns = ['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['sclose']=EMA(df['close'], timeperiod=timePeriod)

    EMA_Value = f"{df['sclose'].tolist()[-1]}"
    time = f"{df['time'].tolist()[-1]}"
    return EMA_Value, time
    