import lxml
import bs4
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

request = requests.get("https://www.vesti.bg/")

soup = bs4.BeautifulSoup(request.text, 'lxml')

titles = set([])
links = set([])
h2 = soup.select('.gtm-TopNews-click')

def scrapeWeb():
       for element in h2:
              title = element.img
              if title is not None:
                     titles.add(title['alt'])
                     links.add(element['href'])

       for link in links:
              rq = requests.get(link)
              article = bs4.BeautifulSoup(rq.text, 'lxml')

              #headline 2: 'subtitle'
              #text: 'article-text', with all the paragraphs separated into different <p></p>


scheduler = BlockingScheduler()
scheduler.add_job(scrapeWeb, 'interval', hours=4)
scheduler.start()