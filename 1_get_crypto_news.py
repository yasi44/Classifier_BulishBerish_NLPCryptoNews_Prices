# -*- coding: utf-8 -*-
import time
import datetime as dt
import json
import glob
import pandas as pd
from flatten_json import flatten
from urllib.request import urlopen
#message notifier
from sendMessage import sendmessage as msg
#import coin list
from getCoinList import getCoinList as coin_list
#message notifier
from sendMessage import sendmessage as msg

#set coin list
#coin_list = coin_list()
# pd.set_option('display.max_columns', None)

filters = ['rising'] #, 'hot', 'bullish', 'bearish', 'important', 'saved', 'lol']

# DEBUGGER
coin_list = ['TRX']
#set coin list
coin_list = coin_list()

pd.set_option('display.max_columns', None)

filters = ['rising', 'hot', 'bullish', 'bearish', 'important', 'saved', 'lol']

# DEBUGGER
# coin_list = ['TRX']

# run every hour
hour = str(dt.datetime.now().hour)
count = True
try:
    while count:
        if(dt.datetime.now().minute == 15):
            print('It\'s ' + hour + ':00!')
            msg('re running News Scraper')
            count = False

    # loop through the coin list
    for c in coin_list:
        try:
            # open file
            filename = './raw_crypto_news/CPNews_' + c + '.csv'
            files_present = glob.glob(filename)

            # check if file exists
            if not files_present:
                # make it
                with open('./raw_crypto_news/filename', 'w+') as in_file:
                    file = pd.DataFrame([in_file])
                    file_start  =  file.shape[0]
                    print('File not exist.',file.shape)
                    pass

            else:
                # or use it
                file = pd.read_csv(filename)
                file = file.drop(columns = 'Unnamed: 0')
                file_start  =  file.shape[0]
                print('File exists',file.shape)

            # loop through the filters
            for f in filters:
                print('Getting', c, f)

                # loop through the pages
                for p in range(10):
                    p = str(p+1)

                    # get data
                    token = '5b92b5faecc605859cc332fc68fd049e0f733768'
                    URL = 'https://cryptopanic.com/api/posts/?auth_token=' + token + \
                          '&currencies=' + c +'&filter=' + f + '&page=' + p + '&public=true&metadata=true'
                    print('Get ...', c, f, 'Page number:',p, 'from:\n',URL)

                    Get_Data_URL = urlopen(URL)
                    data = json.load(Get_Data_URL)

                    # save results
                    results = data['results']

                    # flatten results
                    results = pd.DataFrame([flatten(d) for d in results])

                    # add current time to results
                    results['timestamp'] = str(dt.datetime.now())

                    # append results to df
                    file = file.append(results, ignore_index=True)

                    # drop duplicates
                    file = file.drop_duplicates()

                    # write DataFrame to an csv
                    file.to_csv('./raw_crypto_news/' + filename)

                    print('file size:',file.shape)
                    print('\n')

                # rate limit is 5 req per sec. I'm setting the limit at 4 per sec.
                time.sleep(1/4)

            # How many results did this add?
            file_end = file.shape[0]
            print(file_end - file_start, ' Results added.')
        except:
            msg('ERROR while running get_crypto_news')
    print('Done')
    msg('get_crypto_news is done.')

except :
    pass