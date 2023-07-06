import configparser
import tweepy
from dateutil.relativedelta import relativedelta
import re
import datetime
from nltk.corpus import stopwords
import snscrape.modules.twitter as sntwitter
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) 
stop_words = set(stopwords.words('english'))


class Twitter(object):
    def __init__(self,config = 'analizer\config.ini'):
        self.config_path = config


    def config(self,url):
        config =configparser.RawConfigParser()
        config.read(url)

        api_key = config['twitter']['api_key']
        api_key_secret = config['twitter']['api_key_secret']
        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']

        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
    
        api = tweepy.API(auth)
        return api

    def get_tweets_snc(self, username, end_date):
        start_date = end_date + relativedelta(months=-1)
        number_of_tweets=200
        tweets = []
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username} since:{start_date} until:{end_date}').get_items()):
            if i>number_of_tweets:
                break
            cleaned = clean_text(tweet.rawContent)
            if cleaned:
                tweets.append(cleaned)
        return tweets
        

    def get_tweets(self,username,end_date):
            api = self.config(self.config_path)
            start_date = end_date + relativedelta(months=-1)
            number_of_tweets=200

            tweets = []
            tmpTweets = api.user_timeline(screen_name=username,count=number_of_tweets,exclude_replies = True)
            for tweet in tmpTweets:
                if tweet.created_at.date() < end_date and tweet.created_at.date() > start_date:
                    cleaned = clean_text(tweet.text)
                    if cleaned:
                        tweets.append(cleaned)

            while (tmpTweets[-1].created_at.date() > start_date):
                tmpTweets = api.user_timeline(screen_name=username, count=number_of_tweets,exclude_replies = True, max_id = tmpTweets[-1].id)
                if len(tmpTweets[1:])!=0:
                    for tweet in tmpTweets[1:]:
                        if tweet.created_at.date() <= end_date and tweet.created_at.date() > start_date:
                            cleaned = clean_text(tweet.text)
                            if cleaned:
                                tweets.append(cleaned)
                else:
                    break
            return tweets

def clean_text(text):
        print(text)
        text = text.lower().strip()
        text = re.sub('@[^\s]+','',text)
        text = re.sub('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])','',text)
        text = re.sub('[^\x00-\x7F]+','',text)
        text =  re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub(' +', ' ', text)
        print(text)
        clean_text=""
        for x in text.split():
            if x not in stop_words:
                clean_text=" ".join([clean_text, x])
        print(clean_text)
        doc = nlp(clean_text)
        clean_text=" ".join([token.lemma_ for token in doc])
        print(clean_text)
        return clean_text

