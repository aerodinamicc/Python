import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd
import os

def loadS2():
       news = []
       if os.path.exists('S2.csv'):
              news = pd.read_csv('S2.csv', encoding = 'utf-16')
       return(news)

def scrapeNewArticlesS2(site):
       historyRecords = loadS2()
       
       request = requests.get(site)

       soup = bs4.BeautifulSoup(request.text, 'lxml')

       links = []

       # most read articles
       articles = soup.select('.additional-articles')[0].find_all('ul')[1].select('li') #0 refers to thelast news tab

       for article in articles:
              #title = article.li.div.div.p[1] #the second p element
              link = article.h2.a['href']
              isLinkNone = link is not None
              #For a link to be added, history records should not be empty and link should not have been already added
              if isLinkNone and (len(historyRecords) == 0 or not link in historyRecords.link.values):
                     links.append(link)

       articles = scrapeLinksS2(links) ###!!!

       return(articles)

def scrapeLinksS2(links):
       articlesContent = pd.DataFrame(columns = {'link', 'title', 'comments', 'date', 'hashtags', 'views', 'category'})

       for link in links:
              rq = requests.get(link)
              page = bs4.BeautifulSoup(rq.text, 'lxml')

              #article title
              headline = page.select('h1')[0].text

              #article time
              articleDate = page.select('.article-info')[0].select('p')[0].text

              #category
              category = page.select('.article-info')[0].div.a.text
              views = page.select('.article-info')[0].div.p.text

              #article comments
              comments = page.select('.comments')[0].span.text #adapted

              #article hastags
              tags = page.select('.tags')[0] #adapted, not tested
              tagsList = []
              for tag in tags:
                     if tag != ',' and tag != "\n":
                            tagsList.append(tag.text)

              tagsString = ' - '.join(tagsList)

              #append to articlesContent
              articlesContent = articlesContent.append({'link' : link, 'title': headline,  'comments' : comments, 'date' : articleDate, 'views' : views, 'category' : category, 'hashtags' : tagsString}, ignore_index=True)

       return(articlesContent)

def scrapeS2(site):
       newArticles = scrapeNewArticlesS2(site)
       if os.path.exists('S2.csv'):
              news = pd.read_csv('S2.csv', encoding = 'utf-16')
              news.append(newArticles, ignore_index = True)
              news.to_csv('S2.csv', sep=',', encoding = 'utf-16')
       else:
              newArticles.to_csv('S2.csv', sep=',', encoding = 'utf-16')