# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 01:38:05 2017

@author: varun
"""

import nltk
import numpy as np
import scipy as sp
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import DictVectorizer
import pickle
import feature_extraction


pos_data=np.load('sarcpreproc.npy')
neg_data=np.load('nonsarcpreproc.npy')

print 'Number of  sarcastic tweets :', len(pos_data)
print 'Number of  non-sarcastic tweets :', len(neg_data)

cls_set = ['Non-Sarcastic','Sarcastic']
featuresets = [] 

for tweet in pos_data:
    featuresets.append((feature_extraction.getallfeatureset(tweet),cls_set[1]))
    
for tweet in neg_data:
    featuresets.append((feature_extraction.getallfeatureset(tweet),cls_set[0]))

featuresets=np.array(featuresets)
targets=(featuresets[0::,1]=='Sarcastic').astype(int)

vec = DictVectorizer()
featurevec = vec.fit_transform(featuresets[0::,0])

#Saving the dictionnary vectorizer
file_Name = "vecdict_all.p"
fileObject = open(file_Name,'wb') 
pickle.dump(vec, fileObject)
fileObject.close()

print 'Feature splitting'
#Shuffling
order=shuffle(range(len(featuresets)))
targets=targets[order]
featurevec=featurevec[order,0::]

#Spliting
size = int(len(featuresets) * .3) # 30% is used for the test set

trainvec = featurevec[size:,0::]
train_targets = targets[size:]
testvec = featurevec[:size,0::]
test_targets = targets[:size]

#Artificial weights
pos_p=(train_targets==1)
neg_p=(train_targets==0)
ratio = np.sum(neg_p.astype(float))/np.sum(pos_p.astype(float))
new_trainvec=trainvec
new_train_targets=train_targets
for j in range(int(ratio-1.0)):
    new_trainvec=sp.sparse.vstack([new_trainvec,trainvec[pos_p,0::]])
    new_train_targets=np.concatenate((new_train_targets,train_targets[pos_p]))    

classifier = SVC(C=0.1,kernel='linear')
classifier.fit(new_trainvec,new_train_targets)

#Saving the classifier
file_Name = "classif_all.p"
fileObject = open(file_Name,'wb') 
pickle.dump(classifier, fileObject)
fileObject.close()

print 'Validating'

output = classifier.predict(testvec)
clfreport = classification_report(test_targets, output, target_names=cls_set)
print clfreport
print accuracy_score(test_targets, output)*100


