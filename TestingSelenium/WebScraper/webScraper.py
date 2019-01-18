import lxml
import bs4
import requests
#from sets import Set

request = requests.get("https://www.vesti.bg/")

soup = bs4.BeautifulSoup(request.text, 'lxml')

titles = set([])
links = set([])
h2 = soup.select('.gtm-TopNews-click')

for element in h2:
    #title = element.p
    #if title is not None:
    #    titles.add(title.text)
    #    continue
    title = element.img
    if title is not None:
       titles.add(title['alt'])
       links.add(element['href'])
       continue

print(h2)
print("hi")