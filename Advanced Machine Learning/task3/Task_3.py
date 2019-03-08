#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 22:43:50 2018

"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from imblearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing
import matplotlib.pyplot as plt
import pywt
from sympy import symbols


#Input file names
X_data="X_train.csv"
y_data="y_train.csv"
X_fresh="X_test.csv"

#Import csv files as data frames and set all missing values to zero for now.
df0= pd.read_csv(X_data,header = 0)
df1=pd.read_csv(y_data,header = 0)
df2= pd.read_csv(X_fresh,header = 0)

#%%
#Plot an example time series
#plt.clf()
#plt.show(plt.plot(range(len(df0.values[24,2:])),df0.values[24,2:]))

from biosppy import storage
from biosppy.signals import ecg

# load raw ECG signal
#signal, mdata = storage.load_txt('./examples/ecg.txt')
#plt.clf()
#plt.figure(1)
features=np.zeros((3411,20))
for i in list(range(0,3411)):
    signal=df2.values[i,2:]
    signal=np.delete(signal,np.where(np.isnan(signal)))
    out = ecg.ecg(signal=signal, sampling_rate=300., show=False)
    
    #Make plot of one example heartbeat
    #plt.show(plt.plot(range(len(out['templates'][0])),out['templates'][0]))
    
    w = pywt.Wavelet('db2')
    coeffs = pywt.wavedec(np.mean(out['templates'],axis=0), w,level=4)
    
    
    """
    plt.figure(2)
    def reconstruction_plot(yyy, **kwargs):
        #Plot signal vector on x [0,1] independently of amount of values it contains.
        plt.plot(np.linspace(0, 1, len(yyy)), yyy, **kwargs)
    
    reconstruction_plot(pywt.waverec(coeffs, w)) # full reconstruction 
    #reconstruction_plot(pywt.waverec(coeffs[:-1] + [None] * 1, w)) # leaving out detail coefficients up to lvl 5
    #reconstruction_plot(pywt.waverec(coeffs[:-2] + [None] * 2, w)) # leaving out detail coefficients up to lvl 4
    #reconstruction_plot(pywt.waverec(coeffs[:-3] + [None] * 3, w)) # leaving out detail coefficients up to lvl 3
    reconstruction_plot(pywt.waverec(coeffs[:-4] + [None] * 4, w)) # leaving out detail coefficients up to lvl 2
    #reconstruction_plot(pywt.waverec(coeffs[:-5] + [None] * 5, w)) # leaving out detail coefficients up to lvl 1
    reconstruction_plot(pywt.waverec(coeffs[:-6] + [None] * 6, w)) # leaving out all detail coefficients = reconstruction using lvl1 approximation only
    plt.legend(['Full reconstruction', 'Reconstruction using detail coefficients lvl 1+2', 'Reconstruction using lvl 1 approximation only'])
    """
    
    #Feature Extraction
    coeffs=np.asarray(coeffs)
    
    """
    dummy=coeffs[0]
    for j in list(range(1,5)):
       dummy=np.r_[dummy,coeffs[j]]
    """
    for t in list(range(0,5)):
        features[i,t]=np.amax(coeffs[t])
        features[i,t+5]=np.mean(coeffs[t])
        features[i,t+10]=np.amin(coeffs[t])
        features[i,t+15]=np.std(coeffs[t])
    
    

dftest = pd.DataFrame(features, columns=symbols('x0:20'))
dftest.to_csv('level4_db2_wavedec_coeffs_test.csv',sep=',',float_format='%s',index=False)



raise Exception('exit')
#Extract, from the data frames, the 2D arrays of values
X_traindata=df0.values[:,-1000:]
y_traindata=df1.values[:,1]
X_fresh=df2.values[:,-1000:]

X_train=X_traindata
y_train=y_traindata

wclf=svm.SVC(C=1,kernel='rbf',class_weight='balanced',decision_function_shape='ovo',probability=True)
wclf=wclf.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score
scores = cross_val_score(wclf, X_train, y_train, cv=10,scoring = 'balanced_accuracy',verbose=3,n_jobs=-1)

print(scores.mean())
print(scores.std())
"""
pipeline=Pipeline(steps=[('clf', wclf)])
pipeline=pipeline.fit(X_train, y_train)   

#Use pipeline.get_params().keys() to find how to assign hyperparameters
hyperparameters = {'clf__C':[0.9,0.95,1,1.5]}

grid = GridSearchCV(pipeline, hyperparameters, scoring = 'balanced_accuracy', cv=10,verbose=3,n_jobs=-1)
estimator=grid.fit(X_train,y_train).best_estimator_

#Print the mean cross validated test score of the best combination of parameters from GridSearchCV
print(grid.best_score_)

"""

#Output CSV file
forecast_set=np.matrix(wclf.predict(X_fresh)).T
indexes=df2['id'].values;
dd=np.insert(forecast_set,0,indexes,axis=1)
df=pd.DataFrame(dd)
df.to_csv('forecast.csv',sep=',',float_format='%s',index=False, header=['id','y'])


    
