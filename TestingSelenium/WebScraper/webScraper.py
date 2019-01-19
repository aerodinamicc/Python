import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd
import os
from apscheduler.schedulers.blocking import BlockingScheduler

def scrapeNewArticlesS1():
       request = requests.get("https://www.vesti.bg/")

       soup = bs4.BeautifulSoup(request.text, 'lxml')

       titles = []
       links = []
       h2 = soup.select('.gtm-TopNews-click')

       for element in h2:
              title = element.img
              link = element['href']
              if title is not None:
                     titles.append(title['alt'])
                     links.append(link)

       articles = scrapeLinks(links)
       articles['title'] = titles

       return(articles)

def scrapeLinksS1(links):
       articlesContent = pd.DataFrame(columns = {'link', 'author', 'text', 'subtitle', 'date', 'source'})
       for link in links:
              rq = requests.get(link)
              page = bs4.BeautifulSoup(rq.text, 'lxml')

              #author
              author = page.select('.author') # that returns a list of all elements under class 'author'. We expect only 1 element in return.
              authorName = author[0].img['alt']

              #article text - all the p's in class 'article-text'. We expect only 1 'article-text' element
              article = page.select('.article-text')[0].select('p')
              articleText = ''
              for paragraphIndex in range(len(article)-2):
                     para = str(article[paragraphIndex])
                     if para.startswith('<p dir="ltr" lang="en">'):
                            continue
                     paragraph = para[3:-4] #to exclude <p></p>
                     paragraph = paragraph.replace('\xa0', ' ') #trash
                     articleText = articleText + ' ' + paragraph

              #headline subtitle
              articleSubtitle = page.select('h2.subtitle')[0].text

              #article time
              articleDate = datetime.now().date()

              #article source
              source = page.select('div.article-info-bottom')[0].span #First one is the editor, seond - source
              source = str(source)
              articleSource = ''
              if source is not None:
                     articleSource = source[6:-7]

              #append to articlesContent
              articlesContent = articlesContent.append({'link' : link, 'author' : authorName, 'text' : articleText, 'subtitle' : articleSubtitle, 'date' : articleDate, 'source' : articleSource}, ignore_index=True)

       return(articlesContent)

def scrapeS1():
       newArticles = scrapeNewArticlesS1()

if os.path.exists('S1.csv'):
       news = pd.read_csv('S1.csv', encoding = 'utf-16')
       news.append(newArticles, ignore_index = True)
       news.to_csv('S1.csv', sep=',', encoding = 'utf-16')
else:
       newArticles.to_csv('S1.csv', sep=',', encoding = 'utf-16')

def scrapeNewArticlesS2():
       return()

def scrapeLinksS2(links):
       return()

def scrapeS2():
       return()

def scrapeAll():
       scrapeS1()
       scrapeS2()

scheduler = BlockingScheduler()
scheduler.add_job(scrapeAll, 'interval', hours=12)
scheduler.start()