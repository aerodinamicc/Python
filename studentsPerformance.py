import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
# f, ax = plt.subplots(figsize = (10,10))
# sns.heatmap(st.corr(), annot = True, linewidths= .5, fmt='.2f', ax=ax)
# plt.show()

# st.maths.plot()
# st.reading.plot()
# st.writing.plot(label = "writing", alpha = .5)
# plt.legend(loc = 'lower right')
# plt.xlabel('Students')
# plt.ylabel('Score')
# plt.title("Students' score")

# #Scatter plot
# st.plot(kind = 'scatter', x = 'maths', y = 'reading', alpha = .5, color = 'red')
# st.plot(kind = 'scatter', x = 'writing', y = 'reading', alpha = .5, color = 'green')
# st.loc[:,['maths','reading','writing']].plot()
# st.loc[:,['maths','reading','writing']].plot(subplots = True)
# #Histograms
# st.maths.plot(kind = 'hist', figsize = (6,6), bins = 20)
# plt.show()

#map(func,seq) : applies a function to all the items in a list

# Example of list comprehension
num1 = [1,2,3]
num2 = [i + 1 for i in num1 ]
print(num2)

#group_by
print(st.drop('student', axis = 1).groupby('parentLE').mean())
print(st.groupby(('parentLE', 'prepCourse')).average.mean())
print(st.parentLE.value_counts())

st['race'].replace(regex = True, inplace = True, to_replace = r'\group ', value = r'')
#another option is st['race'] = st['race'].map(lambda x: x.lstrip(group '))
st.parentLE = st.parentLE.replace("bachelor's degree", "BSc") 
st.parentLE = st.parentLE.replace("master's degree", 'MSc')
st.parentLE = st.parentLE.replace("associate's degree", 'Associate')
st.prepCourse = st.prepCourse.replace('none', 'False')
st.prepCourse = st.prepCourse.replace('completed', 'True')

st['race'] = st['race'].astype('category')
st['prepCourse'] = st['prepCourse'].map({'False':False, 'True':True})
st['lunch'] = st['lunch'].astype('category')
st['gender'] = st['gender'].astype('category')
st['parentLE'] = st['parentLE'].astype('category')
print(st.info())

#does preparation matter
fig, axs = plt.subplots(3, 1, sharex=True)
sns.swarmplot(x="gender", y="maths",hue="prepCourse", data=st, ax = axs[0])
sns.swarmplot(x="gender", y="reading",hue="prepCourse", data=st, ax = axs[1])
sns.swarmplot(x="gender", y="writing",hue="prepCourse", data=st, ax = axs[2])
plt.show()

#gender performance across subjects
scores = st.drop(['total', 'average', 'parentLE', 'race', 'lunch'], 1)
scores = pd.melt(scores, ('gender','prepCourse'), ('maths', 'reading', 'writing'))
sns.boxplot(x = "variable", y = 'value', hue = 'gender', data = scores)
plt.xlabel('Subject')
plt.ylabel('Score')
plt.show()

#reading vs writing scores
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
sns.jointplot(st.reading, st.writing, kind="reg", stat_func=r2)
plt.xlabel('Reading scores')
plt.ylabel('Writing scores')
plt.show()

#Math scores higher than average
plt.clf()
maths_higher_than_average = st.gender[st.maths > st.average]
sns.countplot(maths_higher_than_average)
plt.ylabel('Number of students with maths scores higher than their average')
plt.show()

#scores related to race/ethnicity
scores_rel_ethnicity = st.drop(['maths', 'reading', 'writing', 'lunch', 'prepCourse', 'average', 'parentLE', 'student'], 1)

plt.clf()
sns.boxplot(x='gender', y='total', hue = 'race', data = scores_rel_ethnicity)
plt.xlabel('Total score')
plt.show()

#scores related to parents' education
scores_rel_parents = st.drop(['maths', 'reading', 'writing', 'lunch', 'prepCourse', 'average', 'race', 'student'], 1)

plt.clf()
sns.boxplot(x='gender', y='total', hue = 'parentLE', data = scores_rel_parents)
plt.xlabel('Total score')
plt.show()

#race and education
raceEdu = st[['race', 'parentLE']].groupby(['race', 'parentLE']).size().reset_index()
raceEdu.rename(columns = {0 : 'count'}, inplace = True)
raceEdu.pivot_table(values='count', index='race', columns='parentLE')
raceEdu.plot(kind='bar', stacked=True, figsize=(18.5, 10.5))