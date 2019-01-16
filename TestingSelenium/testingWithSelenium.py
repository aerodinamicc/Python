from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://www.seleniumhq.org")
q = driver.find_element_by_id("q")
print("Element with id q:")
print(q)

q_name = driver.find_element_by_name("q")
print("Element with name q:")
print(q_name)

class_name = driver.find_element_by_class_name("selenium-sponsors")
print("Element with class name selenium sponsors:")
print(class_name)

heading = driver.find_element_by_xpath('//*[@id="mainContent"]/h2[1]')
print(heading)

driver.close()
driver.quit()