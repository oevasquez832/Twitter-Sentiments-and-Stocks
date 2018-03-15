import tweepy
import pandas as pd
import numpy as np
import json
import config
from datetime import datetime, timedelta

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Import and Initialize Sentiment Analyzers
from textblob import TextBlob

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()   

#reaching back N days
N = 3

days_ago = datetime.now() - timedelta(days=N)

from dateutil.parser import parse
days = str(days_ago)
dt = parse(days)
converted_time = dt.strftime('%Y-%m-%d')

#input target search here as a list or single term
target_list = ["@CNBC", "@YahooFinance"]
    
    
for item in target_list:
    
    # Lists to hold sentiments, resets for each item in target_list
    compound_list_textblob = []
    compound_list_vader = []
    tweet_times = []    
    text_list = [] 

    for tweet in tweepy.Cursor(api.user_timeline,item).items(1000):
            
        #print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ': ')))
        tweet_text = json.dumps(tweet._json, indent=3)
        tweet = json.loads(tweet_text)
        
        day = parse(str(tweet["created_at"])).strftime('%Y-%m-%d')

        #Run textblob Analysis on each tweet
        results_textblob = TextBlob(tweet["text"])
        results_vader = analyzer.polarity_scores(tweet["text"])
        
        
        
        compound_textblob = results_textblob.sentiment.polarity
        compound_vader = results_vader["compound"]
        #text = tweet["text"] 

        # Add each value to the appropriate list
        compound_list_textblob.append(compound_textblob)
        compound_list_vader.append(compound_vader)
        tweet_times.append(day)
        #text_list.append(text)
        
        #create dictionary to convert into dataframe
        sentiment = {"TextBlob Sentiment Average": compound_list_textblob,
                     "Vader Sentiment Average": compound_list_vader,
                     "Day:": tweet_times}
                    #"Text:": text_list}            
        
    #create the dataframe with column manipulation to group by day and calculate mean
    sent_df = pd.DataFrame.from_dict(sentiment).groupby(['Day:']).mean().reset_index()
    
    #export to csv file for each item in target_list    
    sent_df.to_csv(item + ".csv")