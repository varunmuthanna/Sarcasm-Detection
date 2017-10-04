# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 23:57:27 2017

@author: varun
"""

import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import numpy as np

dict_sad={":-(":"SAD", ":(":"SAD", ":-|":"SAD",  ";-(":"SAD", ";-<":"SAD", "|-{":"SAD"}
dict_happy={":-)":"HAPPY",":)":"HAPPY", ":o)":"HAPPY",":-}":"HAPPY",";-}":"HAPPY",":->":"HAPPY",";-)":"HAPPY"}

wordnet_lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

def replace_emotion(sentence):
    returnsent = sentence    
    for i in dict_happy:
        returnsent = returnsent.replace(i,dict_happy[i])
    for i in dict_sad:
        returnsent = returnsent.replace(i,dict_sad[i])
    return returnsent


def getbigramfeatures(features,sentence):
    tokens = tokenizer.tokenize(sentence)
    lemmas = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    bigrams = nltk.bigrams(lemmas)
    bigrams = [part[0]+' '+part[1] for part in bigrams]
    bigramfeat = lemmas + bigrams
    
    for feat in bigramfeat:
        features['contains(%s)' % feat] = 1.0
        
def gethalfSentimentfeatures(features,sentence):
    tokens = tokenizer.tokenize(sentence)
    
    if len(tokens)==1:
        tokens+=['.']
    f_half = tokens[0:len(tokens)/2]
    s_half = tokens[len(tokens)/2:]
    
    try:
        blob = TextBlob("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in f_half]).strip())

        features['sentiment fhalf'] = blob.sentiment.polarity
        features['subjective fhalf'] = blob.sentiment.subjectivity
        
    except:
        features['sentiment fhalf'] = 0.0
        features['subjective fhalf'] = 0.0
        
    try:
        blob = TextBlob("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in s_half]).strip())

        features['sentiment shalf'] = blob.sentiment.polarity
        features['subjective shalf'] = blob.sentiment.subjectivity
        
    except:
        features['sentiment shalf'] = 0.0
        features['subjective shalf'] = 0.0
        
    features['sentiment halfcontrast'] = np.abs(features['sentiment fhalf'] - features['sentiment shalf'])


def getthirdSentimentfeatures(features,sentence):
    tokens = tokenizer.tokenize(sentence)
    #Split in 3
    if len(tokens)==2:
        tokens+=['.']
    f_half = tokens[0:len(tokens)/3]
    s_half = tokens[len(tokens)/3:2*len(tokens)/3]
    t_half = tokens[2*len(tokens)/3:]
    
    try:
        blob = TextBlob("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in f_half]).strip())

        features['sentiment fthird'] = blob.sentiment.polarity
        features['subjective fthird'] = blob.sentiment.subjectivity
        
    except:
        features['sentiment fthird'] = 0.0
        features['subjective fthird'] = 0.0
        
    try:
        blob = TextBlob("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in s_half]).strip())

        features['sentiment sthird'] = blob.sentiment.polarity
        features['subjective sthird'] = blob.sentiment.subjectivity
        
    except:
        features['sentiment sthird'] = 0.0
        features['subjective sthird'] = 0.0
        
    try:
        blob = TextBlob("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in t_half]).strip())

        features['sentiment tthird'] = blob.sentiment.polarity
        features['subjective tthird'] = blob.sentiment.subjectivity
        
    except:
        features['sentiment tthird'] = 0.0
        features['subjective tthird'] = 0.0
        
    features['sentiment 12contrast'] = np.abs(features['sentiment fthird'] - features['sentiment sthird'])
    features['sentiment 13contrast'] = np.abs(features['sentiment fthird'] - features['sentiment tthird'])
    features['sentiment 23contrast'] = np.abs(features['sentiment sthird'] - features['sentiment tthird'])


def getPOSfeature(features, sentence):
    tokens = tokenizer.tokenize(sentence)

    tokens = [tok.lower() for tok in tokens]
    pos_vector = nltk.pos_tag(tokens)
    vector = np.zeros(4)

    for j in range(len(pos_vector)):
        pos=pos_vector[j][1]
        if pos[0:2] == 'NN':
            vector[0]+=1
        elif pos[0:2] == 'JJ':
            vector[1]+=1
        elif pos[0:2] == 'VB':
            vector[2]+=1
        elif pos[0:2] == 'RB':
            vector[3]+=1
      
    for j in range(len(vector)):
        features['POS' + str(j+1)] = vector[j]

def getCapitalfeature(features,sentence):
    count = 0
    threshold = 4
    for j in range(len(sentence)):
        count +=int(sentence[j].isupper())
    features['Capital'] = int(count>=threshold)

def getExclamationCnt(features,sentence):
    count =0;
    for i in range(len(sentence)):
        count += int(sentence[i] == '!')
    
    features['exclamation'] = count
    
def count_emotion(features,sentence):
    returnsent = sentence
    happy = 0;
    sad = 0    
    for i in dict_happy:
        happy += returnsent.count(i)
    for i in dict_sad:
        sad += returnsent.count(i)
    features['happyemo'] = happy
    features['sademo'] = sad

def getallfeatureset(sent):
    features = {}
    getCapitalfeature(features,sent)
    getExclamationCnt(features,sent)
    count_emotion(features,sent)
    sent = replace_emotion(sent)
    getbigramfeatures(features,sent)
    gethalfSentimentfeatures(features,sent)
    getthirdSentimentfeatures(features,sent)
    getPOSfeature(features,sent)
    return features

#getallfeatureset("The best part of being single is being able to choose any woman I want to shoot me down")