# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 21:10:29 2017

@author: varun
"""

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
import csv
import time
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
# Substitute the values generated from the twitter 
ACCESS_KEY = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''


auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search,
                           q="#sarcasm",
                           rpp=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items():
    if tweet.text[0:2] != 'RT':
        print tweet.text.encode('ascii', 'ignore')
        print "\nmuthannaNewLine\n"