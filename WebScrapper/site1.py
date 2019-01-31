import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd

def gatherNewArticles(site, db):
       request = requests.get(site)
       soup = bs4.BeautifulSoup(request.text, 'lxml')

       titles = []
       links = []
       topNews = soup.select('.gtm-TopNews-click')

       for element in topNews:
              link = element['href']
              title = element.p #something specific, which if not done whould result in duplicating of the article
              if title is not None and (db.empty or (not db.empty and not link in db.link.values)):
                     links.append(link)

       newArticles = crawlLinks(links)

       return(newArticles)

def crawlLinks(links):
       articlesContent = pd.DataFrame(columns = {'link', 'author', 'comments', 'title', 'subtitle', 'date', 'source', 'category', 'systemDate'})
       for link in links:
              rq = requests.get(link)
              if rq.status_code == 200:
                     page = bs4.BeautifulSoup(rq.text, 'lxml')

                     authorName = page.select('.author')[0].img['alt']
                     articleTitle = page.select('h1')[0].text
                     articleSubtitle = page.select('h2.subtitle')[0].text
                     articleDate =  page.select('.article-time')[0].text
                     systemDate = datetime.now().date()
                     source = page.select('div.article-info-bottom')[0].span
                     source = str(source)
                     articleSource = ''
                     if source is not None:
                            articleSource = source[6:-7]

                     category = page.select('div.article-category')[0].a.text

                     comments = page.select('.commentsButtonNumber')[0].text

                     #append to articlesContent
                     articlesContent = articlesContent.append({'link' : link,
                                                               'author' : authorName,
                                                               'comments' : comments,
                                                               'title' : articleTitle,
                                                               'subtitle' : articleSubtitle,
                                                               'date' : articleDate,
                                                               'source' : articleSource,
                                                               'category' : category,
                                                               'systemDate' : systemDate},
                                                               ignore_index=True)

       return(articlesContent)
