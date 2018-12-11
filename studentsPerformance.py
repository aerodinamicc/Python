import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

csvFile = 'StudentsPerformance.csv'
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
print(st.iloc[1:3, 5:7]) #how we do it with integers baby

#uniqueness
print(st['parental level of education'].unique())
print(st['parental level of education'].nunique())
print(st['parental level of education'].value_counts())
print(st.sample(frac = 0.005)) # print random 0.005 % of the dataset
print(st.nlargest(5, 'math score')) # highest 5 math scores

#filters
print(st[(st['math score'] > 95) & (st['reading score'] > 95)])
print(st[np.logical_and(st['math score'] > 95, st['reading score'] > 95)]) #same thing using an np function

#sorting
print(st.sort_values('math score', ascending = False).head())

#renaming columns
st = st.rename(columns = {'parental level of education' : "parentLE", 'race/ethnicity' : 'race', 'test preparation course': 'prepCourse', 'math score' : 'maths', 'reading score': 'reading', 'writing score' : 'writing'})
print(st.columns)
st['total'] = st.maths + st.reading + st.writing
st['average'] = round((st.maths + st.reading + st.writing) / 3, 1)

scores = st.drop(columns = ['gender', 'race', 'parentLE', 'lunch', 'prepCourse'])

#date types
st.parentLE = st.parentLE.astype('category')
st.dtypes

#melt
st['student'] = st.reset_index().index
melted = pd.melt(st, 'student', ('maths', 'reading', 'writing', 'total', 'average')).sort_values('student')

#apply
def isnullvalue(x):
    return(sum(x.isnull()))
print(st.apply(isnullvalue))

#Visualisation
f, ax = plt.subplots(figsize = (10,10))
sns.heatmap(st.corr(), annot = True, linewidths= .5, fmt='1f', ax=ax)
plt.show()

print("end")