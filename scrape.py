# selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# beautiful soup
from bs4 import BeautifulSoup
# time
import time

# set driver path for chromeDriver
service = Service(executable_path="chromedriver.exe")

# Configure Chrome options
options = Options()
# user agent to avoid bot detection 
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument("--headless")  # Enable headless mode

# init chrome driver
driver = webdriver.Chrome(options=options, service=service)


# helper function
def substring(text):
    # skip first 8 chars and get until .
    text = text[8:]
    newString = ""
    for i in text:
        if i == '/':
            newString += '_'
        elif i == '?':
            break
        else:
           newString += i
    newString += ".txt"
    return newString    


# working with the first site using beautiful soup

# target site and load page html
driver.get("https://finance.yahoo.com/markets/stocks/trending/")
#time.sleep(5)
# Wait for all rows to load
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr"))
)
html = driver.page_source
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all 'tr' elements with class 'row false yf-hhhli1' which contain the trending stocks and info
titles = soup.find_all("tr", class_="row false yf-hhhli1")
# titles = soup.select("tr.row.false.yf-hhhli1")

print(f"Number of titles found: {len(titles)}")

# Loop through each title and print relevant info
for title in titles:
    #print(title)
    # Find the ticker symbol of each the % chnage and the volume 
    ticker = title.find('span', class_ = "symbol yf-1fqyif7")
    print(ticker.text)

