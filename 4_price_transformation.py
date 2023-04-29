

import datetime as date
import time
import pprint as pp

import pandas as pd

from talib.abstract import *

#message notifier
from sendMessage import sendmessage as sm

#import coin list
from getCoinList import getCoinList as coin_list

''''
Import processed news articles and respective hourly prices for coin. 
Create columns of differences in the future using .diff() and pct_change().

Column to create:

1 hour
4 hour
12 hour
1 day

'''
#set coin list
coin_list = coin_list()

pd.set_option('display.max_columns', None)

cols = ['close', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'date_time']
for coin in coin_list:
    # get file name
    file = coin + '_price.csv'

    # read file from previous step
    df = pd.read_csv('./price/' + file,
                     usecols=cols,
                     index_col='date_time',
                     engine='c',
                     infer_datetime_format=True,
                     float_precision='round_trip')
    df = df[~df.index.duplicated()]

    df = df.sort_index()

    # rename cols for Abstract API
    # https://github.com/mrjbq7/ta-lib

    inputs = {
        'open': df['open'].values,
        'high': df['high'].values,
        'low': df['low'].values,
        'close': df['close'].values,
        'volume': df['volumefrom'].values
    }

    # uses 9 period close prices
    df['SMA_9_close'] = SMA(inputs, timeperiod=9)

    # uses 25 period close prices (default)
    df['SMA_25_close'] = SMA(inputs, timeperiod=25)

    # uses 50 period close prices
    df['SMA_50_close'] = SMA(inputs, timeperiod=50)

    # uses 100 period close prices
    df['SMA_100_close'] = SMA(inputs, timeperiod=100)

    # uses close prices (default)
    df['bbands_upper'], df['bbands_middle'], df['bbands_lower'] = BBANDS(inputs)

    # uses high, low, close (default)
    df['STOCH_slowk'], df['STOCH_slowD'] = STOCH(inputs) # uses high, low, close by default

    # uses high, low, open instead
    df['STOCH_slowk'], df['STOCH_slowD']  = STOCH(inputs)

    # ADX
    df['ADX_14'] = ADX(inputs, timeperiod=14)

    # ATR
    df['ATR_14'] = ATR(inputs, timeperiod=14)

    # OBV
    df['OBV'] = OBV(inputs)

    # MACD
    df['macd'], df['macdsignal'], df['macdhist'] = MACD(inputs)

    #  MFI
    df['MFI'] = MFI(inputs)

    # RSI
    df['RSI'] = RSI(inputs)

    # MINMAX 365
    df['min_365'], df['max_365'] = MINMAX(inputs, timeperiod=365)

    # MINMAX 180
    df['min_180'], df['max_180'] = MINMAX(inputs, timeperiod=180)

    # MINMAX 90
    df['min_90'], df['max_90'] = MINMAX(inputs, timeperiod=90)

    # MINMAX 30
    df['min_30'], df['max_30'] = MINMAX(inputs, timeperiod=30)

    # MINMAX 14
    df['min_14'], df['max_14'] = MINMAX(inputs, timeperiod=14)

    # MINMAX 7
    df['min_7'], df['max_7'] = MINMAX(inputs, timeperiod=7)

    # HT_TRENDMODE
    df['HT_TRENDMODE']  = HT_TRENDMODE(inputs)

    # create diffs

    df['1_hr_diff'] = df['close'].diff(1)

    df['4_hr_diff'] = df['close'].diff(4)

    df['12_hr_diff'] = df['close'].diff(12)

    df['24_hr_diff'] = df['close'].diff(24)

    # create precent change

    df['1_hr_pct_change'] = df['close'].pct_change(1)

    df['4_hr_pct_change'] = df['close'].pct_change(4)

    df['12_hr_pct_change'] = df['close'].pct_change(12)

    df['24_hr_pct_change'] = df['close'].pct_change(24)

    # create shift in close

    df['close_1'] = df[['close']].shift(1)

    df['close_4'] = df[['close']].shift(4)

    df['close_12'] = df[['close']].shift(12)

    df['close_24'] = df[['close']].shift(24)

    # create isUp column

    df['isUp_1_hr'] = (df[['1_hr_pct_change']] > 0).astype(int)

    df['isUp_4_hr'] = (df[['4_hr_pct_change']] > 0).astype(int)

    df['isUp_12_hr'] = (df[['12_hr_pct_change']] > 0).astype(int)

    df['isUp_24_hr'] = (df[['24_hr_pct_change']] > 0).astype(int)

    # save a new file.
    newfile = 'price_TA_' + coin + '.csv'

    df.to_csv('./price_TA/' + newfile)
    print(coin + ' TA complete')

print('Done')
# sm('finished running priceTechnicalAnalysis.')