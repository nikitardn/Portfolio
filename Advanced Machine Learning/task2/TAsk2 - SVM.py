
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
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
# from imblearn.over_sampling import RandomOverSampler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import balanced_accuracy_score, accuracy_score

TEST_SIZE=0.2
RANDOM_STATE=3
GRID=1
def getData():
    #Input file names
    x_data="X_train.csv"
    y_data="y_train.csv"
    x_fresh="X_test.csv"

    #Import csv files as data frames and set all missing values to the median
    df0= pd.read_csv(x_data,header = 0)
    df1=pd.read_csv(y_data,header = 0)
    df2= pd.read_csv(x_fresh,header = 0)
    indexes = df2['id'].values

    #Extract, from the data frames, the 2D arrays of values
    x_traindata=df0.values[:,-1000:]
    y_traindata=df1.values[:,1]
    x_fresh=df2.values[:,-1000:]
    return x_traindata, y_traindata, x_fresh, indexes


def preprocess_data(x_train, y_train, x_test, x_out):

    #Random resampling
    # ros = RandomOverSampler(random_state=0)
    # x_train, y_train = ros.fit_resample(x_train, y_train)

    # Scaling/Standardizing of the data.
    if 0:
        x_train = preprocessing.scale(x_train)
        x_out = preprocessing.scale(x_out)
        x_test=preprocessing.scale(x_test)
    # Dimensionality reduction
    if 0:
        pca = PCA(n_components=10)
        pca.fit(x_train)
        lda=LinearDiscriminantAnalysis(n_components=10)
        lda.fit(x_train, y_train)
        x_train = pca.transform(x_train)
        x_out = pca.transform(x_out)
        x_test = pca.transform(x_test)
    return x_train, x_test, x_out


def fitdata(x_train, y_train,):
    # Fit a Regression model to the data
    reg = svm.SVC(C=1.0, cache_size=200, class_weight='balanced', coef0=0.0,
                decision_function_shape='ovo', degree=3, gamma='scale', kernel='sigmoid',
                max_iter=-1, probability=False, random_state=None, shrinking=True,
                tol=0.001, verbose=False )
    if GRID:
        grid_params=[{'C': [0.9,0.925,0.95,0.975,1], 'kernel': ['rbf'],'decision_function_shape': ['ovr']}]
                        #{'C': [0.8, 0.9, 1, 1.1, 1.2, 1.4], 'kernel': ['rbf']}
                        #{'C': [0.4, 0.45, 0.5, 0.55, 0.6, 0.65], 'kernel': ['sigmoid'], 'decision_function_shape':['ovo']},
                        #{'C': [ 0.8, 0.825, 0.85, 0.875, 0.9, 0.925], 'kernel': ['rbf'],'decision_function_shape': ['ovo']},
        grid = GridSearchCV(reg, grid_params, scoring='balanced_accuracy', cv=5, verbose=1, n_jobs=-1)
        reg = grid.fit(x_train, y_train).best_estimator_

        print("Best parameters set found on development set:")
        print()
        print(grid.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = grid.cv_results_['mean_test_score']
        stds = grid.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, grid.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))
        print()
    else:
        reg= svm.SVC(C=0.975, cache_size=200, class_weight='balanced', coef0=0.0,
                decision_function_shape='ovo', degree=3, gamma='scale', kernel='rbf',
                max_iter=-1, probability=False, random_state=None, shrinking=True,
                tol=0.001, verbose=False )
        reg.fit(x_train,y_train)
    return reg

def get_scores(reg, x_train, y_train, x_test, y_test):
    # calculate test score
    y_pred = reg.predict(x_test)
    y_pred_train = reg.predict(x_train)
    test_score = balanced_accuracy_score(y_test, y_pred)
    train_score = balanced_accuracy_score(y_train, y_pred_train)
    print("Test score= %s\n", test_score)
    print("train score= %s", train_score)

def predict_output(reg, x_out, indexes):
    #Output CSV file
    forecast_set=np.matrix(reg.predict(x_out)).T
    dd=np.insert(forecast_set,0,indexes,axis=1)
    df=pd.DataFrame(dd)
    df.to_csv('forecast.csv',sep=',',float_format='%s',index=False, header=['id','y'])
    return


def get_plot(reg, y_test, x_test):
    # compute test set deviance
    test_score = np.zeros((NB_ESTIMATORS,), dtype=np.float64)

    for i, y_pred in enumerate(reg.staged_predict(x_test)):
        test_score[i] =   reg.loss_(y_test, y_pred) #r2_score(y_test, y_pred)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Deviance')
    plt.plot(np.arange(NB_ESTIMATORS) + 1, reg.train_score_, 'b-',
             label='Training Set Deviance')
    plt.plot(np.arange(NB_ESTIMATORS)  + 1, test_score, 'r-',
             label='Test Set Deviance')
    plt.legend(loc='upper right')
    plt.xlabel('Boosting Iterations')
    plt.ylabel('Deviance')

    # #############################################################################
    # Plot feature importance
    feature_importance = reg.feature_importances_
    # make importances relative to max importance
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.subplot(1, 2, 2)
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()



if __name__ == '__main__':
    x_data, y_data, x_out, indexes = getData()
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    x_train,  x_test, x_out = preprocess_data(x_train, y_train, x_test, x_out)
    reg = fitdata(x_train, y_train)
    get_scores(reg, x_train, y_train, x_test, y_test)
    # get_plot(reg, y_test, x_test)
    predict_output(reg,x_out, indexes)
    # reg = fitdata(x_data, y_data, )
    # predict_output(reg, x_out, indexes)

