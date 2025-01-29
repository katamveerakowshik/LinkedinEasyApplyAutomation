from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


service = Service(executable_path = 'chromedriver.exe')
driver = webdriver.Chrome()

driver.get("https://www.linkedin.com/login")
time.sleep(2)
driver.find_element(By.ID, "username").send_keys("veerakowshikkatam@gmail.com")
driver.find_element(By.ID, "password").send_keys("9542800259Kk&", Keys.RETURN)
driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20engineer&f_E=2&f_TPR=r86400&f_AL=true")
time.sleep(10)

driver.quit()