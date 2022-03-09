# https://github.com/RonKG/Machine-Learning-Projects-2/blob/master/3.%20NLP_twitter_sentiment_analysis/FINAL____twitter_sentiment_twitter.ipynb
# https://www.kaggle.com/kazanova/sentiment140
# https://www.analyticsvidhya.com/blog/2021/06/twitter-sentiment-analysis-a-nlp-use-case-for-beginners/
# https://github.com/AbhinavThukral97/SentimentAnalysis/blob/master/main.pyhttps://github.com/AbhinavThukral97/SentimentAnalysis/blob/master/main.py

import re
import tweepy
from pathlib import Path
import csv

# twitter api credentials - you need these to gain access to API
"""
consumer_key = '**************************'
consumer_secret = '**************************'
access_token = '**************************'
access_token_secret = '**************************'
"""

# instantiate the api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# string to search on twitter
query = 'batman'
data_folder = Path(FILE_LOCATION)
file_to_write = re.sub(r'[^\w]', '', query) + '_twitter.csv'
file_path = data_folder / file_to_write

# open/create a csv file to append data
csvFile = open(file_path, 'w', encoding='utf-8')

# use csv Writer
csvWriter = csv.writer(csvFile)

# get data from twitter

tweet_num = 0
for tweet in tweepy.Cursor(api.search, q=query, count=10000000, lang="en", tweet_mode='extended').items(10000):
    if tweet.place is not None:
        try:
            # not entirely necessary but you can inspect what is being written to file
            # print('tweet number: {}'.format(tweet_num), tweet.full_text, tweet.place.full_name)
            # write data to csv
            csvWriter.writerow([tweet.created_at,
                                tweet.user.location,
                                tweet.user.followers_count,
                                tweet.user.friends_count,
                                tweet.full_text,
                                tweet.place.bounding_box.coordinates,
                                tweet.place.full_name,
                                tweet.place.country,
                                tweet.place.country_code,
                                tweet.place.place_type])
            tweet_num += 1

        except Exception:
            pass
