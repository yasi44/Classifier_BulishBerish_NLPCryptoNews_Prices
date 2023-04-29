# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

#message notifier
from sendMessage import sendmessage as sm

#import coin list
from getCoinList import getCoinList as coin_list

#set coin list
coin_list = coin_list()

for coin in coin_list:
    # get file name

    # Read in news
    news = pd.read_csv('./processedNews/processed_news_' + coin + '.csv')

    print("reading news for: ", coin)

    # fill na
    news.fillna(0, inplace=True)

    news['created_at'] = news['date_time']

    # set date_time
    news['date_time'] = pd.to_datetime(news['date_time'])

    # set index
    news.set_index('date_time', inplace=True)

    # resample on the hour
    hourly_news = news.resample('H').mean()

    hourly_news = hourly_news.fillna(0)

    # read in prices
    prices = pd.read_csv('./OHLCV_TA/OHLCV_TA_' + coin + '.csv')

    print("reading prices for: ", coin)

    # set date_time
    prices['date_time'] = pd.to_datetime(prices['date_time'])

    # set index
    prices.set_index('date_time', inplace=True)

    # fill na
    prices = prices.fillna(0)

    # merge
    df = pd.merge(hourly_news, prices, left_index=True, right_index=True, how='outer')

    print("merging dataset: ", coin)

    # fill na again
    df = df.replace(np.nan, 0)
    df = df.fillna(0)

    # save a new file.
    newfile = 'clean_data_' + coin + '.csv'

    df.to_csv('./cleaned/' + newfile)
    print("finished with ", coin)

sm('files are cleaned.')