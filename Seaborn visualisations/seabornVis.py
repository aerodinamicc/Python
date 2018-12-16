import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

csvFile = 'StudentsPerformance.csv'
st = pd.read_csv(csvFile)

st = st.rename(columns = {'parental level of education' : "parentLE", 'race/ethnicity' : 'race', 'test preparation course': 'prepCourse', 'math score' : 'maths', 'reading score': 'reading', 'writing score' : 'writing'})

st.parentLE = st.parentLE.astype('category')
st['race'] = st['race'].astype('category')
st['prepCourse'] = st['prepCourse'].astype('category')
st['lunch'] = st['lunch'].astype('category')
st['gender'] = st['gender'].astype('category')

median_house_hold_in_come = pd.read_csv('MedianHouseholdIncome2015.csv', encoding="windows-1252")
percentage_people_below_poverty_level = pd.read_csv('PercentagePeopleBelowPovertyLevel.csv', encoding="windows-1252")
percent_over_25_completed_highSchool = pd.read_csv('PercentOver25CompletedHighSchool.csv', encoding="windows-1252")
share_race_city = pd.read_csv('ShareRaceByCity.csv', encoding="windows-1252")
kill = pd.read_csv('PoliceKillingsUS.csv', encoding="windows-1252")

print(percentage_people_below_poverty_level.head())
print(percentage_people_below_poverty_level.info())
print(percentage_people_below_poverty_level['Geographic Area'].nunique())
print(percentage_people_below_poverty_level['Geographic Area'].unique())

zeros = percentage_people_below_poverty_level['poverty_rate'] == '-'
sum(zeros)
percentage_people_below_poverty_level[zeros] = '0.0'
percentage_people_below_poverty_level['poverty_rate'] = percentage_people_below_poverty_level['poverty_rate'].astype('float')
average_poverty_per_state = percentage_people_below_poverty_level.groupby('Geographic Area').poverty_rate.mean().reset_index()

average_poverty_per_state = average_poverty_per_state.sort_values(['poverty_rate'], ascending = False)

plt.figure(figsize = (13,7))
sns.barplot(x = average_poverty_per_state['Geographic Area'], y = average_poverty_per_state['poverty_rate'])
plt.xlabel('State')
plt.ylabel('Poverty rate')
plt.title('Mean poverty rate across states')
plt.xticks(rotation = 45)

plt.figure(figsize=(13,7))
sns.boxplot(x = 'Geographic Area', y = 'poverty_rate', data = percentage_people_below_poverty_level)

kill.head()
print(kill.name.value_counts())
separate = kill.name[kill.name != 'TK TK'].str.split()
print("a")