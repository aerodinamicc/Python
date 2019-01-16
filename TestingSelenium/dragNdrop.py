from selenium import webdriver
from selenium.webdriver import ActionChains
import time

driver = webdriver.Chrome()
driver.get("http://jqueryui.com/droppable/")
driver.switch_to.frame(0)

action_chain = ActionChains(driver)
draggable = driver.find_element_by_id("draggable")
droppable = driver.find_element_by_id("droppable")

action_chain.drag_and_drop_by_offset(draggable, 50, 50).perform()
time.sleep(2)
action_chain.drag_and_drop(draggable, droppable).perform()

time.sleep(5)

driver.close()
driver.quit()