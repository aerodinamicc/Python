import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd
import os

def loadS4():
       news = []
       if os.path.exists('S4.csv'):
              news = pd.read_csv('S4.csv', encoding = 'utf-16')
       return(news)

def scrapeNewArticlesS4(site):
       historyRecords = loadS4()
       
       request = requests.get(site)

       soup = bs4.BeautifulSoup(request.text, 'lxml')

       links = []

       #most read articles
       mainSection = soup.select(".main-section")[0]
       articles = mainSection.select('.text-news')

       for article in articles:
              #title = article.li.div.div.p[1] #the second p element
              link = article.h2.a['href']
              isLinkNone = link is not None
              #For a link to be added, history records should not be empty and link should not have been already added
              if isLinkNone and (len(historyRecords) == 0 or not link in historyRecords.link.values):
                     links.append(link)

       articles = scrapeLinksS4(links) ###!!!

       return(articles)

def scrapeLinksS4(links):
       articlesContent = pd.DataFrame(columns = {'link', 'title', 'category', 'comments', 'date', 'views'})

       for link in links:
              rq = requests.get(link)
              page = bs4.BeautifulSoup(rq.text, 'lxml')

              #article title
              headline = page.select('.text-wrapper')[0].h2.text

              #metadata
              meta = page.select('.additional-info')[0]

              #author and time
              articleDate = meta.select('.timestamp')[0].text

              #article views
              views = meta.select('#articleViews')[0].text

              #article comments
              comments = meta.select('.comments')[0].text

              #category
              breadCrumbs = page.select('.breadcrumbs')[0].select('li')
              cat = []
              for i in range(1, len(breadCrumbs)):
                  cat.append(breadCrumbs[i].text)

              category = ''.join(cat)
              #no hastags

              #append to articlesContent
              articlesContent = articlesContent.append({'link' : link, 'title' : headline, 'comments' : comments, 'date' : articleDate, 'views' : views, 'category' : category}, ignore_index=True)

       return(articlesContent)

def scrapeS4(site):
       newArticles = scrapeNewArticlesS4(site)
       if os.path.exists('S4.csv'):
              news = pd.read_csv('S4.csv', encoding = 'utf-16')
              news.append(newArticles, ignore_index = True)
              news.to_csv('S4.csv', sep=',', encoding = 'utf-16')
       else:
              newArticles.to_csv('S4.csv', sep=',', encoding = 'utf-16')