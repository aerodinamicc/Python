from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.get("https://wiki.python.org/moin/FrontPage")
search = driver.find_element_by_id("searchinput")
search.send_keys("Beginner")
search.submit()
time.sleep(5)
select = Select(driver.find_element_by_xpath("//*/form/div/select"))
select.select_by_visible_text("Raw Text")

print("end")