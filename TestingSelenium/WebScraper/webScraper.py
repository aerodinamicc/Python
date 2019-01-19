import lxml
import bs4
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def scrapeWeb():
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

       scrapeArticles(links)

def scrapeArticles(links):
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
                     para = article[paragraphIndex]
                     paragraph = str(para)[3:-4] #to exclude <p></p>
                     articleText = articleText + ' ' + paragraph

              #headline 2: 'subtitle'
              
              #article time
              articleDate = datetime.now().date()

scrapeWeb()
#scheduler = BlockingScheduler()
#scheduler.add_job(scrapeWeb, 'interval', hours=4)
#scheduler.start()