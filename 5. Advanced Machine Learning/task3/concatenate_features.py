import numpy as np
import pandas as pd
import biosppy as bio
import time
#Input file names
x_file1="X_train_extracted.csv"
x_file2="level4_db2_wavedec_coeffs.csv"
x_file3="X_train_extracted_hr.csv"
x_file4="X_train_counts.csv"
x_test_file1="X_test_extracted.csv"
x_test_file2="level4_db2_wavedec_coeffs_test.csv"
x_test_file3="X_test_extracted_hr.csv"
x_test_file4="X_test_counts.csv"
LOAD=True

df01= pd.read_csv(x_file1,header = None)
df02= pd.read_csv(x_file2,header = 0)
df03= pd.read_csv(x_file3,header = None)
df04= pd.read_csv(x_file4,header = None)

df11= pd.read_csv(x_test_file1,header = None)
df12= pd.read_csv(x_test_file2,header = 0)
df13= pd.read_csv(x_test_file3,header = None)
df14= pd.read_csv(x_test_file4,header = None)

s0=np.sum(df04.values,axis=1)
s1=np.sum(df14.values,axis=1)

s0=np.matrix(s0).T
s1=np.matrix(s1).T

df04=np.divide(df04.values,np.asarray(s0).astype(float))
df14=np.divide(df14.values,np.asarray(s1).astype(float))

x_train=np.concatenate((df01.values,df02.values,df03.values,df04),axis=1)
x_test=np.concatenate((df11.values,df12.values,df13.values,df14),axis=1)

np.savetxt("X_train_concat.csv", x_train, delimiter=",",fmt='%5.2f')
np.savetxt("X_test_concat.csv", x_test, delimiter=",",fmt='%5.2f')