import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd

def gatherNewArticles(site, db):
       request = requests.get(site)
       soup = bs4.BeautifulSoup(request.text, 'lxml')

       links = []

       mainSection = soup.select(".main-section")[0]
       articles = mainSection.select('.text-news')

       for article in articles:
              link = article.h2.a['href']
              #isLinkNone = link is not None
              if db.empty or (not db.empty and not link in db.link.values):
                     links.append(link)

       articles = crawlLinks(links)

       return(articles)

def crawlLinks(links):
       articlesContent = pd.DataFrame(columns = {'link', 'title', 'category', 'comments', 'date', 'views', 'systemDate'})

       for link in links:
              rq = requests.get(link)
              if rq.status_code == 200:
                     page = bs4.BeautifulSoup(rq.text, 'lxml')
                     headline = page.select('.text-wrapper')[0].h2.text
                     meta = page.select('.additional-info')[0]
                     articleDate = meta.select('.timestamp')[0].text
                     systemDate = datetime.now().date()
                     views = meta.select('#articleViews')[0].text
                     comments = meta.select('.comments')[0].text
                     #category
                     breadCrumbs = page.select('.breadcrumbs')[0].select('li')
                     cat = []
                     for i in range(1, len(breadCrumbs)):
                            cat.append(breadCrumbs[i].text)

                     category = ''.join(cat)

                     #no hastags

                     #append to articlesContent
                     articlesContent = articlesContent.append({'link' : link,
                                                               'title' : headline,
                                                               'comments' : comments,
                                                               'date' : articleDate,
                                                               'views' : views,
                                                               'category' : category,
                                                               'systemDate' : systemDate}, 
                                                               ignore_index=True)

       return(articlesContent)