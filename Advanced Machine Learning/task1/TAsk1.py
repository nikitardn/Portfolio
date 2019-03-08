
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 22:57:09 2018

"""
import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import RFECV
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline



OUTLIERS_NB_NEIGHBOURS = 200
OUTLIERS_CONTAMINATION=0.1
NB_FEATURES=100
TEST_SIZE=0.01
RANDOM_STATE=0
def getData():
    #Input file names
    x_data="X_train.csv"
    y_data="y_train.csv"
    x_fresh="X_test.csv"

    #Import csv files as data frames and set all missing values to the median
    df0= pd.read_csv(x_data,header = 0)
    df0=df0.fillna(df0.median())
    df1=pd.read_csv(y_data,header = 0)
    df1=df1.fillna(df1.median())
    df2= pd.read_csv(x_fresh,header = 0)
    df2=df2.fillna(df2.median())
    indexes = df2['id'].values;

    #Extract, from the data frames, the 2D arrays of values
    x_traindata=df0.values[:,-887:]
    y_traindata=df1.values[:,1]
    x_fresh=df2.values[:,-887:]
    return x_traindata, y_traindata, x_fresh, indexes


def preprocess_data(x_train, y_train, x_out):
    # Outlier Detection - Create a classifier. Tune number of neighbors and contamination proportion.
    # Outlier_bool is an array containing 1s and -1s. -1 indicates an outlier, and 1 indicates an inlier
    outlier_clf = LocalOutlierFactor(n_neighbors=OUTLIERS_NB_NEIGHBOURS, contamination=OUTLIERS_CONTAMINATION)
    outlier_bool = outlier_clf.fit_predict(x_train)

    # Processed training data that contains only the inliers
    x_train_inliers = np.delete(x_train, np.where(outlier_bool == -1), axis=0)
    y_train_inliers = np.delete(y_train, np.where(outlier_bool == -1), axis=0)

    # Scaling/Standardizing of the data.
    x_train_scaled=preprocessing.scale(x_train_inliers)
    x_out_scaled=preprocessing.scale(x_out)

    # Select K best features based on the F_regression method and keep only those in the training data
    selector = SelectKBest(f_regression, k=NB_FEATURES)
    x_train_selected=selector.fit_transform(x_train_scaled,y_train_inliers)
    x_out_selected = x_out_scaled[:,selector.get_support(indices=True)]
    return x_train_selected, x_out_selected, y_train_inliers



def fitdata(x, y,):
    # Now that pre-processing is done, perform test train split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=TEST_SIZE)
    # Fit a Regression model to the data
    ##reg=RandomForestRegressor(n_jobs=-1,n_estimators=160)
    rfecv=RFECV(estimator=LinearRegression(), scoring='r2',step=5)
    reg=Pipeline([('poly', PolynomialFeatures(degree=2)), ('polyfit', rfecv)])

    # reg=svm.SVR(kernel='linear')
    reg.fit(x_train, y_train)
    print(rfecv.n_features_, rfecv.grid_scores_)
    # calculate test score
    y_pred = reg.predict(x_test)
    score = r2_score(y_test, y_pred)
    print("score= %s", score)
    return reg

def predict_output(reg, x_out, indexes):
    #Output CSV file
    forecast_set=np.matrix(reg.predict(x_out)).T
    dd=np.insert(forecast_set,0,indexes,axis=1)
    df=pd.DataFrame(dd)
    df.to_csv('forecast.csv',sep=',',float_format='%s',index=False, header=['id','y'])
    return

if __name__ == '__main__':
    x_data, y_data, x_out, indexes = getData()
    x_selected, x_out_selected, y_inliers= preprocess_data(x_data, y_data, x_out)
    reg = fitdata(x_selected, y_inliers,)
    predict_output(reg,x_out_selected, indexes)
    # reg = fitdata(x_data, y_data, )
    # predict_output(reg, x_out, indexes)

