# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 00:20:04 2017

@author: varun
"""

#from textblob import TextBlob



#wiki = TextBlob(" to shoot me down")
#print wiki.sentiment

import numpy as np
import pickle
import os
import feature_extraction
#import topic


file1 = open('vecdict_all.p', 'r')
file2 = open('classif_all.p','r')

vec = pickle.load(file1)
classifier = pickle.load(file2)

file1.close()
file2.close()

#sentence = "I never miss the lecture of Dan Moldovan"
#sentence = "Donald trump will make america great again"
#sentence = "Messi is the best footballer in the world"
#sentence = "Oh how I love being ignored"
#sentence = "Absolutely adore it when my bus is late"
#sentence = "I work 40 hours a week to be this poor"
def getSarcasmScore(sentence):
    sentence = sentence.encode('ascii', 'ignore')
    features = feature_extraction.getallfeatureset(sentence)
    
    features_vec = vec.transform(features)
    score = classifier.decision_function(features_vec)[0]
    percentage = int(round(2.0*(1.0/(1.0+np.exp(-score))-0.5)*100.0))
    
    return percentage

while True:
    print "enter the sentence to get sarcastic score or type exit to quit"
    data = str(raw_input())
    if data == "exit":
        break;
    else:
        print getSarcasmScore(data)
