# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot
import numpy as np
from sklearn.ensemble import RandomForestClassifier
# %matplotlib inline
errors='coerce'

df = pd.read_csv('./analysis/BTC.csv')
df.drop(columns='Unnamed: 0', inplace=True)


df = df.rename(index=str, columns={"votes_disliked": "dislike",
                              "votes_important": "important",
                              "votes_liked": "liked",
                              "votes_lol": "lol",
                              "votes_negative": "bearish",
                              "votes_positive": "bullish",
                              "votes_saved": "saved",
                              "votes_toxic": "toxic"})
df['user_sent_opinions'] = df['bearish'] + df['bullish']

df['bullishness'] = ((df['bullish'] / df['user_sent_opinions']) * 100)

df['bearishness'] = -((df['bearish'] / df['user_sent_opinions']) * 100)
df.drop(list(df.filter(regex = 'isUp_')), axis = 1, inplace = True)
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(0)
df = df.replace(np.nan, 0)
# create a list of target cols for predictions

target_cols = ['dislike', 'important',
       'liked', 'lol', 'bearish', 'bullish',
       'saved', 'toxic']

targets = df[target_cols]
X_features = df.drop(columns=target_cols)
X_features.drop(columns=['date_time','bullishness', 'bearishness', 'user_sent_opinions'], inplace=True)
targets['user_sent_opinions'] = targets['bearish'] + targets['bullish']
targets['bullishness'] = ((targets['bullish'] / targets['user_sent_opinions']) * 100)
targets['is_bullish'] = np.where(targets['bullishness'] >= 60, 1, 0)
targets.drop(columns=['bullishness', 'bullish', 'bearish'], inplace=True)

print(dir(RandomForestClassifier()))
print(RandomForestClassifier())

# Predict on if is_bullish or not
# with Cross-Validation
from sklearn.model_selection import KFold, cross_val_score
rf = RandomForestClassifier(n_jobs=-1)
k_fold = KFold(n_splits=5)
cross_val_score(rf, X_features, targets['is_bullish'], cv=k_fold, scoring='accuracy', n_jobs=-1)

# with Fscore
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test =  train_test_split(X_features, targets['is_bullish'], test_size=0.2)
rf = RandomForestClassifier(n_estimators=150, max_depth=None, n_jobs=-1)
rf_model = rf.fit(X_train, y_train)
most_imp_feats = pd.DataFrame(sorted(zip(rf_model.feature_importances_, X_train.columns), reverse=True)[0:20])
y_pred = rf_model.predict(X_test)
precision, recall, fscore, support = score(y_test, y_pred, average='binary')
print('Precision: {} / Recall: {} / Accuracy {}'.format(round(precision, 3),
                                                   round(recall, 3),
                                                   round((y_pred==y_test).sum() / len(y_pred),3)))
print('Precision --> our classifier identified an article as Bullish it was Bullish {}% of the time.'
      .format(round((precision*100), 1)))
print('Recall --> all of the bullish articles {}% where identified by classifier.'
      .format(round((recall)*100, 1)))
print('Accuracy --> of all the articles classifier predicted them to be bullish correctly {}% of the time.'
      .format(round(round((y_pred==y_test).sum() / len(y_pred),3)*100),1))

# most_imp_feats = most_imp_feats.rename(index=str, columns={0: "Importance",
#                                                            1: "Feature"})
# # #most_imp_feats.set_index('Feature', inplace=True)
# # most_imp_feats.plot.barh(x='Feature', y="Importance");