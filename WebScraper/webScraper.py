import lxml
import bs4
import requests
from datetime import datetime
import pandas as pd
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import site1
import site2
import site3

def scrapeAll():
       print(os.getcwd())
       sites = open('WebScraper/sites.txt', 'r')

       webPage1 = sites.readlines(1)[0][:-2] # -2 helps clean \n at the end of each line 
       #site1.scrapeS1(webPage1)

       webPage2 = sites.readlines(2)[0][:-2]
       #site2.scrapeS2(webPage2)

       webPage3 = sites.readlines(3)[0][:-2]
       site3.scrapeS3(webPage3)

scrapeAll()
#scheduler = BlockingScheduler()
#scheduler.add_job(scrapeAll, 'interval', hours=12)
#scheduler.start()