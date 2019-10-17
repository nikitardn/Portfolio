#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:55:53 2018

@author: yanni
"""

import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.neighbors import LocalOutlierFactor
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from imblearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier

#Input file names
X_data="features_train_flow_all2.csv"
y_data="targets_all_flow.csv"
X_fresh="features_test_flow_all2.csv"


#Import csv files as data frames and set all missing values to zero for now.
df0= pd.read_csv(X_data,header=None)
df1= pd.read_csv(y_data,header=None)
df2= pd.read_csv(X_fresh,header=None)

X_train=df0.values[:,:]
y_train = df1.values[:,1]
X_fresh=df2.values[:,:]


#selector=SelectKBest(f_regression,k=100)
#X_train=selector.fit_transform(X_train,y_train)
#X_fresh=X_fresh[:,selector.get_support(indices=True)]
#X_fresh=selector.transform(X_fresh)

print('done extracting')
clf1=RandomForestClassifier(n_estimators=800,max_features='auto',max_depth=20,
                           min_samples_split=4,min_samples_leaf=3,bootstrap=True)

clf2=GradientBoostingClassifier(n_estimators=1200)

clf=AdaBoostClassifier(clf1,n_estimators=10000)

#clfB=AdaBoostClassifier(clf2,n_estimators=10000)

sfm=SelectFromModel(clf,0.0008)
X_train=sfm.fit_transform(X_train,y_train)
X_fresh=sfm.transform(X_fresh)

rkf = RepeatedKFold(n_splits=2, n_repeats=5)
scores = cross_val_score(clf2, X_train, y_train, cv=rkf,scoring ='roc_auc',verbose=3,n_jobs=-1)

print(scores.mean())
print(scores.std())
print(scores.min())
print(scores.max())

estimator=clf2.fit(X_train, y_train)   

#Output CSV file

d={'id':range(0,len(df2)),'col0':estimator.predict_proba(X_fresh)[:,0],'col1':estimator.predict_proba(X_fresh)[:,1]}
df=pd.DataFrame(d)
df=df.drop(columns=['col0'])
df.to_csv('forecast.csv',sep=',',float_format='%s',index=False, header=['id','y'])

