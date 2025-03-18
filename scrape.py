from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# set driver path for chromeDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# set target site
driver.get("https://google.com")

# always quit driver
driver.quit()