from selenium import webdriver

driver = webdriver.Chrome(executable_path = "G:/Python/TestingSelenium/chromedriver.exe")
driver.maximize_window()
driver.get("https://www.google.com")
driver.find_element_by_name("q").send_keys("zlatan angelov")
driver.find_element_by_name("btnK").click()

print(driver.title)

driver.close()
driver.quit()