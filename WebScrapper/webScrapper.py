#from apscheduler.schedulers.blocking import BlockingScheduler
import os
import pandas as pd
import numpy as np
from datetime import datetime
import site1
import site2
import site3
import site4

def loadDb(siteIndex):
       dbString = "S%s.csv" % (siteIndex)

       if os.path.exists(dbString):
              news = pd.read_csv(dbString, encoding = 'utf-16')

              if 'Unnamed: 0' in news.columns:
                     news.drop(['Unnamed: 0'], axis = 1, inplace = True)

              return(news)
       
       return pd.DataFrame()

def saveDb(siteIndex, newArticles, db):
       dbString = "S%s.csv" % (siteIndex)
       scraped_printout = "Site %s has %s new articles." % (siteIndex, len(newArticles))
       #print(scraped_printout)
       global message
       message = message + scraped_printout + "\n"

       if os.path.exists(dbString):
              #if there are new articles
              if not newArticles.empty:
                     news = db.append(newArticles, sort=True, ignore_index = True)
                     news.to_csv(dbString, sep=',', encoding = 'utf-16', index = False)
              #in any other case(no new articles/update)
              elif newArticles.empty and not db.empty:
                     db.to_csv(dbString, sep=',', encoding = 'utf-16', index = False)
       else:
              newArticles.to_csv(dbString, sep=',', encoding = 'utf-16')

def updateDb(siteIndex, webPage, db):
       isSiteOne = siteIndex == 1

       db.systemDate = db.systemDate.apply(lambda x: datetime.strptime(x, '%Y-%m-%d') if len(x) < 11 else
                                                datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
       #only if the 3,7,14 days have passed
       db['timeSincePublishing'] = (db.systemDate - datetime.now()).apply(lambda x: abs(x.days))

       #3 days old, last condition is because I only want to update what has not yet been updated (comments and views are equally reliable)
       threeDaysOld = db[(db['timeSincePublishing'] > 2) & (db['timeSincePublishing'] < 4) & (np.isnan(db['3daysComments'].values))].reset_index().rename(columns = {'index' : 'position'})
       articlesIndices = threeDaysOld.position.values
       threeDaysOld = updateLinks(siteIndex, threeDaysOld.link.values)
       threeDaysOld['position'] = articlesIndices

       for i in threeDaysOld.position:
              db.loc[i, '3daysComments'] = threeDaysOld.comments[threeDaysOld.position == i].values[0]
              if not isSiteOne:
                     db.loc[i, '3daysViews'] = threeDaysOld.views[threeDaysOld.position == i].values[0]

       #7 days old
       oneWeekOld = db[(db['timeSincePublishing'] > 6) & (db['timeSincePublishing'] < 8) & (np.isnan(db['1weekComments'].values))].reset_index().rename(columns = {'index' : 'position'})
       articlesIndices = oneWeekOld.position.values
       oneWeekOld = updateLinks(siteIndex, oneWeekOld.link.values)
       oneWeekOld['position'] = articlesIndices

       for i in oneWeekOld.position:
              db.loc[i, '1weekComments'] = oneWeekOld.comments[oneWeekOld.position == i].values[0]
              if not isSiteOne:
                     db.loc[i, '1weekViews'] = oneWeekOld.views[oneWeekOld.position == i].values[0]

       #14 days old
       twoWeeksOld = db[(db['timeSincePublishing'] > 13) & (db['timeSincePublishing'] < 15) & (np.isnan(db['2weeksComments'].values))].reset_index().rename(columns = {'index' : 'position'})
       articlesIndices = twoWeeksOld.position.values
       twoWeeksOld = updateLinks(siteIndex, twoWeeksOld.link.values)
       twoWeeksOld['position'] = articlesIndices
       
       for i in twoWeeksOld.position:
              db.loc[i, '2weeksComments'] = twoWeeksOld.comments[twoWeeksOld.position == i].values[0]
              if not isSiteOne:
                     db.loc[i, '2weeksViews'] = twoWeeksOld.views[twoWeeksOld.position == i].values[0]

       db.drop(['timeSincePublishing'], axis=1, inplace = True)
       updated_printout = "Site %s has %s articles updated." % (siteIndex, len(threeDaysOld) + len(oneWeekOld) + len(twoWeeksOld))
       #print(updated_printout)
       global message
       message = message + updated_printout + "\n"
 
       return(db)

def updateLinks(siteIndex, links):
       newData = pd.DataFrame()
       if siteIndex == 1:
              newData = site1.updateLinks(links)
       elif siteIndex == 2:
              newData = site2.updateLinks(links)
       elif siteIndex == 3:
              newData = site3.updateLinks(links)
       elif siteIndex == 4:
              newData = site4.updateLinks(links)
       
       return(newData)

def crawlSite(siteIndex, webPage):
       db = loadDb(siteIndex)

       #Let's update (views and comments) the db first
       if not db.empty:
              db = updateDb(siteIndex, webPage, db)
       
       newArticles = pd.DataFrame()

       if siteIndex == 1:
              newArticles = site1.gatherNewArticles(webPage, db)
       elif siteIndex == 2:
              newArticles = site2.gatherNewArticles(webPage, db)
       elif siteIndex == 3:
              newArticles = site3.gatherNewArticles(webPage, db)
       elif siteIndex == 4:
              newArticles = site4.gatherNewArticles(webPage, db)
       
       saveDb(siteIndex, newArticles, db)

def iterateSites():
       start_message = "Newspaper boy dispatched..."
       print(start_message)
       global message
       message = message + start_message + "\n"

       abspath = os.path.abspath(__file__)
       dname = os.path.dirname(abspath)
       os.chdir(dname)
       with open('sites.txt', 'r') as sites:
              for siteIndex in range(1, 5):
                     webPage = ''
                     if siteIndex != 4:
                            webPage = sites.readlines(siteIndex)[0][:-2] # -2 helps clean \n at the end of each line 
                     else:
                            webPage = sites.readlines(siteIndex)[0]

                     crawlSite(siteIndex, webPage)

message = ""
iterateSites()

final_message = 'Stay classy San Diego.'
print(final_message)
message = message + final_message

import smtplib, ssl

with open('mail.txt', 'r') as mail:
       elements = mail.read().split("\n")
       sender = elements[0]
       password = elements[1]
       receiver = elements[2]

       context = ssl.create_default_context()
       with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
              server.login(sender, password)
              server.sendmail(sender, receiver, message)

