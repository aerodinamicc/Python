import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd

def gatherNewArticles(site, db):
       request = requests.get(site)
       soup = bs4.BeautifulSoup(request.text, 'lxml')

       links = []

       tabwidget = a = soup.select(".tabwidget")[0]
       articles = tabwidget.select('article')

       for article in articles:
              link = article.a['href']
              if db.empty or (not db.empty and not link in db.link.values):
                     links.append(link)

       articles = crawlLinks(links)

       return(articles)

def crawlLinks(links):
       articlesContent = pd.DataFrame(columns = {'link', 'title', 'location', 'category', 'comments', 'date', 'hashtags', 'views', 'systemDate',
                                                 '3daysComments', '1weekComments', '2weeksComments', '3daysViews', '1weekViews', '2weeksViews'})

       for link in links:
              rq = requests.get(link)
              if rq.status_code == 200:
                     page = bs4.BeautifulSoup(rq.text, 'lxml')

                     headline = page.select('.post-title')[0].text

                     #metadata
                     simpleShare = page.select('.simple-share')[0]
                     li = simpleShare.find_all('li')
                     location = li[0].text
                     articleDate = li[1].text
                     systemDate = datetime.now()
                     views = li[2].text
                     views = views.replace(" прочита", "")
                     comments = li[3].text
                     comments = comments.replace(" коментара", "")
                     breadCrumbs = page.select('.breadcrumb')[0]
                     category = breadCrumbs.find_all('span')
                     if len(category) > 3:
                            category = category[3].text
                     else:
                            category = ""

                     #article hastags
                     tags = page.select('.tag-link') #adapted, not tested
                     tagsList = []
                     for tag in tags:
                            tagsList.append(tag.text)

                     tagsString = ' - '.join(tagsList)

                     #append to articlesContent
                     articlesContent = articlesContent.append({'link' : link,
                                                               'title' : headline,
                                                               'location' : location,
                                                               'comments' : comments,
                                                               'date' : articleDate,
                                                               'views' : views,
                                                               'category' : category,
                                                               'hashtags' : tagsString,
                                                               'systemDate' : systemDate},
                                                               ignore_index=True)

       return(articlesContent)

def updateLinks(links):
       updatedContent = pd.DataFrame(columns = {'link', 'views', 'comments'})
       for link in links:
              rq = requests.get(link)
              if rq.status_code == 200:
                     page = bs4.BeautifulSoup(rq.text, 'lxml')

                     #metadata
                     simpleShare = page.select('.simple-share')[0]
                     li = simpleShare.find_all('li')
                     if len(li) < 4: #IF THE ARTICLE has been deleted and the rq.tet is the website's main page
                            views = 'NaN'
                            comments = 'NaN'
                     else:
                            views = li[2].text
                            views = views.replace(" прочита", "")
                            comments = li[3].text
                            comments = comments.replace(" коментара", "")
                     
                     #append to articlesContent
                     updatedContent = updatedContent.append({'link' : link,
                                                               'views' : views,
                                                               'comments' : comments},
                                                               ignore_index=True)

       return(updatedContent)