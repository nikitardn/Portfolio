import numpy as np
import pandas as pd
import biosppy as bio
import time
#Input file names
x_file="X_train.csv"
y_file="y_train.csv"
x_test_file="X_test.csv"
LOAD=True

#Import csv files as data frames
if LOAD:
    df0=np.load('df0.npy')
    df1=np.load('df1.npy')
    df2=np.load('df2.npy')
else:
    df0= pd.read_csv(x_file,header = 0)
    df1=pd.read_csv(y_file,header = 0)
    df2= pd.read_csv(x_test_file,header = 0)

    np.save('df0', df0)
    np.save('df1', df1)
    np.save('df2', df2)


    df0=df0.values
    df1=df1.values
    df2=df2.values

y_train = df1[:, 1]
N=y_train.size
m=180

#Extract, from the data frames, the 2D arrays of values
t = time.time()

xy_train=[]
for i in list(range(0,N)):
    y=y_train[i]
    sig=df0[i,1:]
    sig=np.delete(sig,np.where(np.isnan(sig)))
    out = bio.ecg.ecg(signal=sig, sampling_rate=300., show=False)

    beats=out['templates']
    nb=beats.shape[0]
    # mean_beat=np.mean(beats,0)
    # var_beat=np.var(beats,0)
    # x_train[i,:]=np.concatenate((mean_beat,var_beat))
    heart_rate=out['heart_rate']
    rpeaks=sig[out['rpeaks']]
    max_r=rpeaks.max()
    min_r = rpeaks.max()
    mean_r = np.mean(rpeaks.max())
    var_r = np.var(rpeaks.max())
    if heart_rate.size==0:
        hr_mean = 0
        hr_var = 0
        hr_min = 0
        hr_max = 0
    else:
        hr_mean=np.mean(heart_rate)
        hr_var=np.var(heart_rate)
        hr_min=heart_rate.min()
        hr_max=heart_rate.max()
    features=np.array([hr_mean,hr_var,hr_max,hr_min,mean_r,var_r,max_r,min_r])
    features.shape=(1,8)
    xy_train.append(features)
    if i % 100==0:
        print(i*100/N)
np.savetxt("X_train_extracted_hr.csv", np.concatenate(xy_train,axis=0), delimiter=",",fmt='%5.2f')
print('Done Training')

N=df2.shape[0]
#Extracting features for test data
xy_test=[]
for i in list(range(0,N)):
    sig=df2[i,1:]
    sig=np.delete(sig,np.where(np.isnan(sig)))
    out = bio.ecg.ecg(signal=sig, sampling_rate=300., show=False)
    beats=out['templates']
    heart_rate = out['heart_rate']
    rpeaks=sig[out['rpeaks']]
    max_r=rpeaks.max()
    min_r = rpeaks.max()
    mean_r = np.mean(rpeaks.max())
    var_r = np.var(rpeaks.max())

    if heart_rate.size==0:
        hr_mean = 0
        hr_var = 0
        hr_min = 0
        hr_max = 0
    else:
        hr_mean=np.mean(heart_rate)
        hr_var=np.var(heart_rate)
        hr_min=heart_rate.min()
        hr_max=heart_rate.max()

        features = np.array([hr_mean, hr_var, hr_max, hr_min, mean_r, var_r, max_r, min_r])
    features.shape=(1,8)
    xy_test.append(features)
    if i % 100==0:
        print(i*100/N)
np.savetxt("X_test_extracted_hr.csv", np.concatenate(xy_test,axis=0), delimiter=",",fmt='%5.2f')