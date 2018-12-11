import numpy as np
import pandas as pd
import os

csvFile = 'StudentsPerformance.csv'

pd.read_csv(csvFile)
st = pd.read_csv(csvFile)
type(csvFile)
st.shape
st.info()
print(st.describe())
print(st.quantile(0.95))

#how much so far *=
print(st['math score'].cumprod())

#how much so far +=
print(st['math score'].cumsum())

#null
print(sum(st['math score'].isnull()))
print(st.isnull())

#corr
print(st.corr())

#subsetting
print(st[3:13])
print(st.iloc[[3], [3]])
print(st.iloc[[1,3],[4,5]])
print(st[[1,3],[4,5]])
print(st.iloc[1:3, 5:7]) #how we do it with integers baby
print(st[3:14, 1:5])

#uniqueness
print(st['parental level of education'].unique())
print(st['parental level of education'].nunique())
print(st['parental level of education'].value_counts())
print(st.sample(frac = 0.005)) # print random 0.005 % of the dataset
print(st.nlargest(5, 'math score')) # highest 5 math scores

#filters
print(st[(st['math score'] > 95) & (st['reading score'] > 95)])
print(st[np.logical_and(st['math score'] > 95, st['reading score'] > 95)]) #same thing using an np function
print("end")