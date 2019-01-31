#from apscheduler.schedulers.blocking import BlockingScheduler
import os
import pandas as pd
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

       if os.path.exists(dbString):
              #if there are new article
              if not newArticles.empty:
                     news = db.append(newArticles, ignore_index = True)
                     news.to_csv(dbString, sep=',', encoding = 'utf-16', index = False)
              #in any other case(no new articles/update)
              elif newArticles.empty and not db.empty:
                     db.to_csv(dbString, sep=',', encoding = 'utf-16', index = False)
       else:
              newArticles.to_csv(dbString, sep=',', encoding = 'utf-16')

def updateDb(siteIndex, webPage, db):
       db.systemDate = db.systemDate.apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
       db['timeSincePublishing'] = (db.systemDate - datetime.now().date()).apply(lambda x: abs(x.days))
       sub = db[(db['timeSincePublishing'] > 13) & (db['timeSincePublishing'] < 15)]
       sub = updateLinks(siteIndex, sub.link.values)
       
       for i in sub.index:
              db.loc['comments',i] = sub.loc['comments',i]
              db.loc['views',i] = sub.loc['views',i]

       db.drop(['timeSincePublishing'], axis=1, inplace = True)

       return(db)

def updateLinks(siteIndex, links):
       newData = pd.DataFrame()
       if siteIndex == 1:
              newData = site1.crawlLinks(links)
       elif siteIndex == 2:
              newData = site2.crawlLinks(links)
       elif siteIndex == 3:
              newData = site3.crawlLinks(links)
       elif siteIndex == 4:
              newData = site4.crawlLinks(links)
       
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
       os.chdir('WebScrapper')
       sites = open('sites.txt', 'r')
       print(os.getcwd())

       for siteIndex in range(1, 5):
              webPage = ''
              if siteIndex != 4:
                     webPage = sites.readlines(siteIndex)[0][:-2] # -2 helps clean \n at the end of each line 
              else:
                     webPage = sites.readlines(siteIndex)[0]

              crawlSite(siteIndex, webPage)

iterateSites()

print('end')
#scheduler = BlockingScheduler()
#scheduler.add_job(scrapeAll, 'interval', hours=12)
#scheduler.start()