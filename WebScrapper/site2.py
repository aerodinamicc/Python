import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd

def gatherNewArticles(site, db):
       request = requests.get(site)
       soup = bs4.BeautifulSoup(request.text, 'lxml')

       links = []

       articles = soup.select('.additional-articles')[0].find_all('ul')[1].select('li') #0 refers to thelast news tab

       for article in articles:
              link = article.h2.a['href']
              if db.empty or (not db.empty and not link in db.link.values):
                     links.append(link)

       articles = crawlLinks(links)

       return(articles)

def crawlLinks(links):
       articlesContent = pd.DataFrame(columns = {'link', 'title', 'comments', 'date', 'hashtags', 'views', 'category', 'systemDate',
                                                 '3daysComments', '1weekComments', '2weeksComments', '3daysViews', '1weekViews', '2weeksViews'})

       for link in links:
              rq = requests.get(link)
              if rq.status_code == 200:
                     page = bs4.BeautifulSoup(rq.text, 'lxml')

                     headline = page.select('h1')[0].text
                     articleDate = page.select('.article-info')[0].select('p')[0].text
                     systemDate = datetime.now().date()
                     category = page.select('.article-info')[0].div.a.text
                     views = page.select('.article-info')[0].div.p.text
                     views = views.replace("Прегледи: ", "")
                     comments = page.select('.comments')[0].span.text
                     tags = page.select('.tags')[0] #adapted, not tested
                     tagsList = []
                     for tag in tags:
                            if tag != ',' and tag != "\n":
                                   tagsList.append(tag.text)

                     tagsString = ' - '.join(tagsList)

                     #append to articlesContent
                     articlesContent = articlesContent.append({'link' : link,
                                                               'title': headline,
                                                               'comments' : comments,
                                                               'date' : articleDate,
                                                               'views' : views,
                                                               'category' : category,
                                                               'hashtags' : tagsString,
                                                               'systemDate' : systemDate},
                                                               ignore_index=True)

       return(articlesContent)

