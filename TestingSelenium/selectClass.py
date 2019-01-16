from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.get("https://www.computerhope.com/jargon/d/dropdm.htm")
select = Select(driver.find_element_by_id("s"))

time.sleep(2)
select.select_by_index(1)
time.sleep(2)
select.select_by_visible_text("Choice 3")
time.sleep(2)
print(select.options)

print("end")
