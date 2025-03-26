# selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# beautiful soup
from bs4 import BeautifulSoup
# time
import time

# set driver path for chromeDriver
service = Service(executable_path="chromedriver.exe")

# Configure Chrome options
options = Options()
# options.add_argument("--headless")  # Enable headless mode

# init chrome driver
driver = webdriver.Chrome(options=options, service=service)

# make array of target sites 
sites = ["https://finance.yahoo.com/markets/stocks/trending/", 
         "https://finance.yahoo.com/markets/stocks/gainers/", 
         "https://finance.yahoo.com/markets/stocks/most-active/",
         "https://finance.yahoo.com/topic/stock-market-news/",
         "https://www.marketwatch.com/",
         "https://www.marketwatch.com/column/need-to-know?mod=newsviewer_click",
         "https://seekingalpha.com/editors-picks",
         "https://seekingalpha.com/market-news/trending",
         "https://www.bloomberg.com/markets",
         "https://www.reddit.com/r/wallstreetbets/",
         "https://www.reddit.com/r/stocks/",
         "https://www.reddit.com/r/investing/",
         "https://finviz.com/",
         "https://finviz.com/news.ashx",
         "https://finviz.com/screener.ashx?v=120&s=ta_topgainers"
        ]


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

''''
# loop array and open each site
for site in sites:
  # set target site
  driver.get(site)
  # write site HTML to file 
  path = "site-html\\" + substring(site)
  #path = "site-html\data.txt"
  file = open(path, "w", encoding="utf-8")
  file.write(driver.page_source)
  file.close()'
'''''

# working with the first site using beautiful soup
# https://finance.yahoo.com/markets/stocks/trending/

# target site and load page html
driver.get("https://finance.yahoo.com/markets/stocks/trending/")
time.sleep(20)
html = driver.page_source
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all 'tr' elements with class 'row false yf-hhhli1' which contain the trending stocks and info
titles = soup.find_all("tr", class_="row false  yf-hhhli1")

print(f"Number of titles found: {len(titles)}")

# Loop through each title and print relevant info
for title in titles:
    print(title)
    # Find the ticker symbol of each the % chnage and the volume 
    ticker = title.find('span', class_ = "symbol yf-1fqyif7")
    print(ticker.text)



# close site
# driver.quit()

