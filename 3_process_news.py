# -*- coding: utf-8 -*-
import pandas as pd
import glob
import time
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import regex as re
from textblob import TextBlob
from readcalc import readcalc
from sklearn.feature_extraction.text import TfidfVectorizer

pd.set_option('display.max_columns', None)

# from bdateutil import isbday
# import holidays

# message notifier
# from sendMessage import sendmessage as sm

# import coin list
from getCoinList import getCoinList as coin_list


# set coin list
# coin_list = coin_list()

# functions

# .get polarity calculation for textblob
def polarity_calc(text):
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return None


# .get subjectivity calculation for textblob
def subjectivity_calc(text):
    try:
        return TextBlob(text).sentiment.subjectivity
    except:
        return None


# .get assessment calculation for textblob
def assessment_calc(text):
    try:
        return TextBlob(text).sentiment_assessments
    except:
        return None


# get scores calculation for ReadCalc
def get_smog_score(text):
    return (readcalc.ReadCalc(text).get_smog_index())


def get_coleman_liau_score(text):
    return (readcalc.ReadCalc(text).get_coleman_liau_index())


# .get_smog_index()
# .get_flesch_reading_ease()
# .get_flesch_kincaid_grade_level()
# .get_coleman_liau_index()
# .get_gunning_fog_index()
# .get_ari_index()
# .get_lix_index()
# .get_dale_chall_score()

# example
# get_scores(14).get_smog_index()

def text_to_wordlist(text, remove_stopwords=False):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(text).get_text()
    #
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]", " ", review_text)
    #
    # 3. Convert words to lower case and split them
    words = review_text.lower().split()
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    #
    # 5. Return a string of words
    #
    string = " ".join(str(x) for x in words)

    return (string)

# Dataframe of user scored articles scrapped from Crytpopanic
cols = ['created_at', 'domain', 'metadata_description',
       'source_domain', 'source_title',
       'title', 'votes_disliked', 'votes_important', 'votes_liked',
       'votes_lol', 'votes_negative', 'votes_positive', 'votes_saved',
       'votes_toxic']

# glob.glob('data*.csv') - returns List[str]
# pd.read_csv(f) - returns pd.DataFrame()
# for f in glob.glob() - returns a List[DataFrames]
# pd.concat() - returns one pd.DataFrame()
news = pd.concat([pd.read_csv(f) for f in glob.glob('./raw_crypto_news/CPNews_*.csv')], ignore_index = True)

news = news[cols]
coin = 'ALL'

# get rid of inf, na, and nan
news = news.replace([np.inf, -np.inf], np.nan)
news = news.fillna(0)
news = news.replace(np.nan, 0)

# drop the first row ('its full of Nans')
# news = news[1:]

# creat features, prep columns

# clean text
news['title'] = news['title'].astype(str).replace('<p>', '')

news['metadata_description'] = news['metadata_description'].astype(str).replace('<p>', '')

# get length of title and description
news['title_len'] = [len(t) for t in news['title']]

news['desc_len'] = [len(t) for t in news['metadata_description']]

# news['metadata_description'] = news['metadata_description']


# get readablity factors

# Smog Index
news['title_smog_score'] = news['title'].apply(get_smog_score);

news['description_smog_score'] = news['metadata_description'].apply(get_smog_score);

# Coleman Liau Index
news['title_coleman_liau_score'] = news['title'].apply(get_coleman_liau_score);

news['description_coleman_liau_score'] = news['metadata_description'].apply(get_coleman_liau_score);


# get sentiment related factors for the title from Textblob

news['title_polarity'] = news['title'].apply(polarity_calc)

news['title_subjectivity'] = news['title'].apply(subjectivity_calc)


# get sentiment related factors for the description from Textblob

news['description_polarity'] = news['metadata_description'].apply(polarity_calc)

news['description_subjectivity'] = news['metadata_description'].apply(subjectivity_calc)

# check is business day in varius regions

# news['biz_day_in_us'] = news['created_at'].map(lambda x: int(isbday(x, holidays=holidays.US())))

# news['biz_day_in_china'] = news['created_at'].map(lambda x: int(isbday(x, holidays=holidays.CH())))

# news['biz_day_in_korea'] = news['created_at'].map(lambda x: int(isbday(x, holidays=holidays.SK())))

# news['biz_day_in_japan'] = news['created_at'].map(lambda x: int(isbday(x, holidays=holidays.JP())))

# news['biz_day_in_uk'] = news['created_at'].map(lambda x: int(isbday(x, holidays=holidays.UK())))


# make dummy columns for domains etc...

# news = pd.concat([news, pd.get_dummies(news['domain'], dummy_na=True, prefix='domain_')], axis=1)

# news = pd.concat([news, pd.get_dummies(news['source_domain'], dummy_na=True, prefix='source_domain_')], axis=1)

# news = pd.concat([news, pd.get_dummies(news['source_title'], dummy_na=True, prefix='source_title_')], axis=1)


# creating TFIDF Vectorizer and Corpus
title_corpus = news['title']

# Fit the transformer
tvec_title = TfidfVectorizer(stop_words='english',
                             max_features=2000,
                             max_df = .1,
                             ngram_range=(1,3))

tvec_title.fit(title_corpus)

title_corpus_df  = pd.DataFrame(tvec_title.transform(title_corpus).todense(),
                   columns=tvec_title.get_feature_names(),
                   index=news.index)

news = pd.merge(news, title_corpus_df, left_index=True, right_index=True, how='outer', suffixes=('_news', '_title'))

del title_corpus_df

desc_corpus = news['metadata_description']

# Fit the transformer
tvec_desc = TfidfVectorizer(stop_words='english',
                             max_features=2000,
                             max_df = .1,
                             ngram_range=(1,3))

tvec_desc.fit(desc_corpus)

desc_corpus_df  = pd.DataFrame(tvec_desc.transform(desc_corpus).todense(),
                   columns=tvec_desc.get_feature_names(),
                   index=news.index)

news = pd.merge(news, desc_corpus_df, left_index=True, right_index=True, how='outer', suffixes=('_news', '_desc'))

del desc_corpus_df

# final clean up
# round time to nearest hour
news['date_time'] = pd.to_datetime(news['created_at'])# .dt.round("H")

# create a days of week column
news['day_of_week'] = news['date_time'].dt.weekday_name

# dummy days of week
news = pd.concat([news, pd.get_dummies(news['day_of_week'], dummy_na=True, prefix='is')], axis=1)

# set index
news.set_index('date_time', inplace=True)

# drop unneeded columns
droppable = ['created_at','domain', 'metadata_description','source_domain', 'source_title'] # , 'day_of_week', 'is_nan'

news = news.drop(columns=droppable)

timestr = time.strftime("%Y%m%d-%H%M%S")

# save a new file.
newfile = 'processed_news_' + coin + '_' + timestr + '.csv'

news.to_csv('./processedNews/' + newfile)

print('All Done')
#sm('finished running processsCryptoPanicNews.')