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

       #top article
       links.append(soup.select('div.main-news')[0].a['href'])

       #secondary articles
       secondaryArticles = soup.select('.topic')[0:6]

       for article in secondaryArticles:
              #title = article.li.div.div.p[1] #the second p element
              link = article.a['href']
              isLinkNone = link is not None
              #For a link to be added, history records should not be empty and link should not have been already added
              if isLinkNone and (len(historyRecords) == 0 or not any(link in l for l in historyRecords.link)):
                     links.append(link)

       articles = scrapeLinksS2(links) ###!!!

       return(articles)

def scrapeLinksS2(links):
       articlesContent = pd.DataFrame(columns = {'link', 'author', 'comments', 'date', 'source',  'hashtags', 'views'})

       for link in links:
              rq = requests.get(link)
              page = bs4.BeautifulSoup(rq.text, 'lxml')

              #author
              author = page.select('.author')[0] # that returns a list of all elements under class 'author'. We expect only 1 element in return.
              authorName = author.a.span.text

              #article title
              headline = page.select('h1')[0].text

              #article time
              articleDate = datetime.now().date()

              #category
              category = page.select('.article-info')[0].div.a.text
              views = page.select('.article-info')[0].div.p.text

              #article comments
              comments = page.select('.comments')[0].span.text #adapted

              #article hastags
              tags = page.select('.tags')[0] #adapted, not tested
              tagsStr = []
              for tag in tags:
                     if tag != ',':
                            tagsStr.append(tag.text)
              #append to articlesContent
              articlesContent = articlesContent.append({'link' : link, 'author' : authorName, 'comments' : comments, 'date' : articleDate, 'views' : views, 'category' : category, 'hashtags' : tags}, ignore_index=True)

       return(articlesContent)

def scrapeS2(site):
       newArticles = scrapeNewArticlesS2(site)
       if os.path.exists('S2.csv'):
              news = pd.read_csv('S2.csv', encoding = 'utf-16')
              news.append(newArticles, ignore_index = True)
              news.to_csv('S2.csv', sep=',', encoding = 'utf-16')
       else:
              newArticles.to_csv('S2.csv', sep=',', encoding = 'utf-16')