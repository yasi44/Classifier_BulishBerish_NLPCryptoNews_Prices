# -*- coding: utf-8 -*-
import time
import datetime
import json
import glob
import pprint as pp
import pandas as pd
from flatten_json import flatten
from urllib.request import urlopen, Request

#message notifier
from sendMessage import sendmessage as msg

#import coin list
from getCoinList import getCoinList as coin_list

#set coin list
coin_list = coin_list()

for coin in coin_list:
    try:
        print('Getting', coin)

        now = str(pd.Timestamp.now().floor('60min').to_pydatetime())
        ts = time.strptime(now, '%Y-%m-%d  %H:%M:%S')
        timestamp = str(time.mktime(ts)) # works
        print('Starting at: ', datetime.datetime.fromtimestamp(int(float(timestamp))).strftime('%Y-%m-%d %H:%M'))

        keep_going = True
        TimeFrom = timestamp
        new_dict = pd.DataFrame()

        while keep_going:

            url = 'https://min-api.cryptocompare.com/data/histohour?fsym=' + coin +\
                  '&tsym=USD&limit=2000&toTs=' + timestamp + '&extraParams=leroi'
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req)

            data = json.load(webpage)

            # grab a few variables that I need for the loop

            #TimeTo = data['TimeTo']
            TimeFrom = data['TimeFrom']
            timestamp = str(TimeFrom + 3600)
            print('Collecting: ', datetime.datetime.fromtimestamp(int(float(timestamp))).strftime('%Y-%m-%d %H:%M'))

            # create a new dict out of the data I need
            new_dict = new_dict.append(pd.DataFrame({item['time']:item for item in data['Data'][1:]}).T)
            keep_going = data['Data'][1]['close'] != 0

        df = new_dict
        df['date_time'] = pd.to_datetime(df['time'],unit='s')
        df.set_index('time', inplace=True)
        df.sort_index(ascending=False, inplace=True)

        # write DataFrame to an csv
        df.to_csv('./price/' + coin + 'price.csv')
    #     print(df.shape)
    #     df.head()

    # rate limit is 15 req per sec. I'm setting the limit at 14 per sec.
        time.sleep(1/14)
    except:
        msg('ERROR while running get_price.')
print('Done')
msg('Done running get_Price')