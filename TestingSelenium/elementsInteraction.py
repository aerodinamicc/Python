from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("http://www.python.org")
search = driver.find_element_by_name("q")
search.clear()
search.send_keys("pandas")
search.submit()

driver.close()
driver.quit()
