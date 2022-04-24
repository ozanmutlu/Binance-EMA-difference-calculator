import ccxt
import pandas as pd
from talib import EMA
import pandas_ta

def getEMA(coin, timeFrame, timePeriod, Algorithm):
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        },
    })

    ohlc = exchange.fetch_ohlcv(coin, timeframe=timeFrame)
    df = pd.DataFrame(ohlc, columns = ['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    if Algorithm == 'Pandas':
        df['sclose'] = pandas_ta.ema(df['close'], length=timePeriod, talib=False)
    else:
        df['sclose']=EMA(df['close'], timeperiod=timePeriod)

    EMA_Value = f"{df['sclose'].tolist()[-1]}"
    time = f"{df['time'].tolist()[-1]}"
    return EMA_Value, time
    