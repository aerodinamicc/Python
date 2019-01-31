#from apscheduler.schedulers.blocking import BlockingScheduler
import os
import pandas as pd
import site1
import site2
import site3
import site4

def loadDb(siteIndex):
       dbString = "S%s.csv" % (siteIndex)

       if os.path.exists(dbString):
              news = pd.read_csv(dbString, encoding = 'utf-16', index_col='Unnamed: 0')
              return(news)
       
       return pd.DataFrame()

def saveDb(siteIndex, newArticles):
       dbString = "S%s.csv" % (siteIndex)

       if os.path.exists(dbString):
              news = pd.read_csv(dbString, encoding = 'utf-16')
              news = news.append(newArticles, ignore_index = True)
              news.to_csv(dbString, sep=',', encoding = 'utf-16')
       else:
              newArticles.to_csv(dbString, sep=',', encoding = 'utf-16')

def crawlSite(siteIndex, webPage):
       db = loadDb(siteIndex)
       
       newArticles = pd.DataFrame()

       if siteIndex == 1:
              newArticles = site1.gatherNewArticles(webPage, db)
       elif siteIndex == 2:
              newArticles = site2.gatherNewArticles(webPage, db)
       elif siteIndex == 3:
              newArticles = site3.gatherNewArticles(webPage, db)
       elif siteIndex == 4:
              newArticles = site4.gatherNewArticles(webPage, db)
       
       saveDb(siteIndex, newArticles)

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