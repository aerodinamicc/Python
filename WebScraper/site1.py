import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd
import os

def loadS1():
       news = []
       if os.path.exists('S1.csv'):
              news = pd.read_csv('S1.csv', encoding = 'utf-16')
       return(news)

def scrapeNewArticlesS1(site):
       historyRecords = loadS1()
       
       request = requests.get(site)

       soup = bs4.BeautifulSoup(request.text, 'lxml')

       titles = []
       links = []
       topNews = soup.select('.gtm-TopNews-click')

       for element in topNews:
              title = element.img
              link = element['href']
              isTitleNone = title is not None
              if isTitleNone:
                     #in case the app is run for the first time and recrods are empty
                     if len(historyRecords) == 0:
                            titles.append(title['alt'])
                            links.append(link)
                     #for any subsequent update of the db
                     else:
                            if not title.isin(historyRecords.title) and not link.isin(historyRecords.link):
                                   titles.append(title['alt'])
                                   links.append(link)
                            elif not title.isin(historyRecords.title) and link.isin(historyRecords.link):
                                   linkIndex = historyRecords.link.index(link)
                                   historyRecords['title'][linkIndex] = title

       articles = scrapeLinksS1(links)
       articles['title'] = titles

       return(articles)

def scrapeLinksS1(links):
       articlesContent = pd.DataFrame(columns = {'link', 'author', 'comments', 'title', 'subtitle', 'date', 'source', 'category'})
       for link in links:
              rq = requests.get(link)
              page = bs4.BeautifulSoup(rq.text, 'lxml')

              #author
              author = page.select('.author') # that returns a list of all elements under class 'author'. We expect only 1 element in return.
              authorName = author[0].img['alt']

              #headline subtitle
              articleTitle = page.select('h1')[0].text
              articleSubtitle = page.select('h2.subtitle')[0].text

              #article time
              articleDate = datetime.now().date()

              #article source
              source = page.select('div.article-info-bottom')[0].span #First one is the editor, seond - source
              source = str(source)
              articleSource = ''
              if source is not None:
                     articleSource = source[6:-7]

              #article category
              category = page.select('div.article-category')[0].a.text

              #article comments
              comments = page.select('.commentsButtonNumber')[0].text

              #append to articlesContent
              articlesContent = articlesContent.append({'link' : link, 'author' : authorName, 'comments' : comments, 'title' : articleTitle, 'subtitle' : articleSubtitle, 'date' : articleDate, 'source' : articleSource, 'category' : category}, ignore_index=True)

       return(articlesContent)

def scrapeS1(site):
       newArticles = scrapeNewArticlesS1(site)
       if os.path.exists('S1.csv'):
              news = pd.read_csv('S1.csv', encoding = 'utf-16')
              news.append(newArticles, ignore_index = True)
              news.to_csv('S1.csv', sep=',', encoding = 'utf-16')
       else:
              newArticles.to_csv('S1.csv', sep=',', encoding = 'utf-16')
