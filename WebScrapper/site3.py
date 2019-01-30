import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd
import os

def loadS3():
       news = []
       if os.path.exists('S3.csv'):
              news = pd.read_csv('S3.csv', encoding = 'utf-16')
       return(news)

def scrapeNewArticlesS3(site):
       historyRecords = loadS3()
       
       request = requests.get(site)

       soup = bs4.BeautifulSoup(request.text, 'lxml')

       links = []

       #most read articles
       tabwidget = a = soup.select(".tabwidget")[0]
       articles = tabwidget.select('article')

       for article in articles:
              #title = article.li.div.div.p[1] #the second p element
              link = article.a['href']
              isLinkNone = link is not None
              #For a link to be added, history records should not be empty and link should not have been already added
              if isLinkNone and (len(historyRecords) == 0 or not link in historyRecords.link.values):
                     links.append(link)

       articles = scrapeLinksS3(links) ###!!!

       return(articles)

def scrapeLinksS3(links):
       articlesContent = pd.DataFrame(columns = {'link', 'title', 'location', 'category', 'comments', 'date', 'hashtags', 'views'})

       for link in links:
              rq = requests.get(link)
              page = bs4.BeautifulSoup(rq.text, 'lxml')

              #article title
              headline = page.select('.post-title')[0].text

              #metadata
              simpleShare = page.select('.simple-share')[0]
              li = simpleShare.find_all('li')

              #location
              location = li[0].text

              #article time
              articleDate = li[1].text

              #article views
              views = li[2].text

              #article comments
              comments = li[3].text

              #category
              breadCrumbs = page.select('.breadcrumb')[0]
              category = breadCrumbs.find_all('span')[3].text

              #article hastags
              tags = page.select('.tag-link') #adapted, not tested
              tagsList = []
              for tag in tags:
                     tagsList.append(tag.text)

              tagsString = ' - '.join(tagsList)

              #append to articlesContent
              articlesContent = articlesContent.append({'link' : link, 'title' : headline, 'location' : location, 'comments' : comments, 'date' : articleDate, 'views' : views, 'category' : category, 'hashtags' : tagsString}, ignore_index=True)

       return(articlesContent)

def scrapeS3(site):
       newArticles = scrapeNewArticlesS3(site)
       if os.path.exists('S3.csv'):
              news = pd.read_csv('S3.csv', encoding = 'utf-16')
              news.append(newArticles, ignore_index = True)
              news.to_csv('S3.csv', sep=',', encoding = 'utf-16')
       else:
              newArticles.to_csv('S3.csv', sep=',', encoding = 'utf-16')