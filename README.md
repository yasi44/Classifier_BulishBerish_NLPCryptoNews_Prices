# Classifier_BulishBerishPredictor_NLPCryptoNews_Prices

## Objective
To Predict if we publish a news, it will have a 'Berish' or 'Bulish' feedback from users :D

## Solution
To train a clasifier model that based on news published and the crypto currency price behavior can determine if a news will be tagged as a 'Bulish' or 'Perish' by users.

## Data
  Assumption about data: News need at least one week to be considered as mature(means we can process them), because users have given enough votes for them. 
### Price Data and Price-related extra metrics
  - Collected from  CryptoCompare.com API.
  - Availability of data: daily, hourly and minutely(available only for 7 days) increments.
  - Here we focus on hourly data.
  - Since price may not be a sufficient metric, we need to collect more metrics. Thats why we used TA-lib(includes 200 indicators such as ADX, MACD, RSI, Stochastic, Bollinger Bands etc... and candlestick pattern recognition)
  - More metrics: Predictor columns from the pricing data using .diff(), .pct_change() and .shift() from the pandas library.
  - Traders respond to technical indicators and news associated with an asset. Therefore here we create columns to reflect indicator values associated with a given coin.
    RSI (Relative Strength Index) (standard periods, 14 )
    SMA (Simple Moving Average) 9, 25, 50, 100 period
    Bollinger Bands (standard periods)
    Stochastic Strength Indicator (standard periods)
    ADX Average Daily Direction (standard periods, 14)
    ATR Average True Range (standard periods, 14)
    OBV Observed Buy Volume
    MACD Moving Average Convergence Divergence
    MFI Money Flow Index
    Min Max (Minimum and Maximum price over the last n days
    365 day
    180 day
    90 day
    30 day
    14 day
    7 day
    HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
  - 
    * close_n --> price n hours ago.
    * min_n --> minimum price Bitcoin has reached in the last n days.
    * max_n --> maximum price Bitcoin has reached in the last n days.
    * SMA_n_close --> Simple Moving Average on the close price over a period of n days.

### News Data and News-related extra metrics
  - Here the used articles sourced from Cryptopanic.com. This website contains a collection of opinions, and posts related to cryptocurrencies and blockchain technologies from various online sources(eddit, Twitter, Bitcoin.com, CCN.com, Coindesk.com, Ethereumworldnews.com, Dailyhodl.com, and WSJ.com, CryptoPanic) in different languages. Articles are sorted based on content(specific for a coin or coins), and it enables users to express their opinion of the article by voting on it. Eight voting options available for users: 
    - like
    - dislike
    - bullish --> user believe that an article has a Bulish impact on the price of the associated currency
    - berish --> user believe that an article has a Berish impact on the price of the associated currenc
    - important
    - lol
    - toxic
    - saved
  - Besides the voting information from each user, Cryptopanic.com only provides description and title of news.
  - Extera metrics:
    * Measure of readability of the article(high readability score causes user to read and understand an article) using two readability scoring methods. 
      . Smog Index (https://en.wikipedia.org/wiki/SMOG)
      . Coleman Liau Index (https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index)
    * Polarity and subjectivity of the title and description(acquired using textblob).
      . polarity has a range of (-1, 1)
      . subjectivity has a range of (0, 1)
      . Create 1-hot-encode for all domains and authors

### Dummy columns added to represent date specific variables
    Day of week (0-6)
    is day a business day (1,0)
    code adapted from jckantor/NYSE_tradingdays.py
    time of day (0-23)

## Predictions
    is Bullish values are >= 65
    is Bearish values are <= 35
    otherwise neutral
    important (continuous)
    is the article toxic (1,0)
    is liked (1,0)
    is disliked
    will the article have an impact on price in the next:
    1 hr
    4 hrs
    12 hrs
    24 hours


## Predict on 'is_bullish'  --> here we use Random Forest Classifier, but I will include ensemple methods
### Results:
  - Precision --> 81.6% of all the prediction the model made, were Bulish
  - Recall --> 88.0% of all Bulish articled were detected/predicted correctly
  - Accuracy --> 79.0% of all the articles that are predicted as being Bulish, are predicted correctly
