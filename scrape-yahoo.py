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
import re

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

# loop yahoo sites and output data to file
# target sites and load page html
targets = ["https://finance.yahoo.com/markets/stocks/trending/", "https://finance.yahoo.com/markets/stocks/gainers/", 
           "https://finance.yahoo.com/markets/stocks/most-active/"]
with open("output.txt", "w") as file:
    for target in targets: 
        file.write(f"{target}\n")
        driver.get(target)
        # Wait for all rows to load
        #WebDriverWait(driver, 20).until(
            #EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr"))
        #)

        #WebDriverWait(driver, 30)
        html = driver.page_source
        #driver.quit()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find all 'tr' elements with class 'row false yf-hhhli1' which contain the trending stocks and info
        #titles = soup.find_all("tr", class_="row false yf-hhhli1")
        #titles = soup.find_all("tr", class_="row yf-cfbsv7")
        titles = soup.find_all("tr", class_=re.compile(r"row.*yf-"))

        # Loop through each title and print relevant info
        for title in titles:
            # Find the ticker symbol, % change, and volume
            #ticker = title.find('span', class_="symbol yf-1fqyif7")
            #ticker = title.find('span', class_="symbol yf-86iz4a")
            ticker = title.find('span', class_=re.compile(r"symbol.*yf-"))
            #change = title.select_one('[data-field="regularMarketChangePercent"] span')
            #volume = title.select_one('[data-field="regularMarketVolume"] span')
            change = title.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
            volume = title.find('fin-streamer', {'data-field': 'regularMarketVolume'})

            # Extract text only if the element exists
            ticker_text = ticker.text.strip() if ticker else "N/A"
            change_text = change.text.strip() if change else "N/A"
            volume_text = volume.text.strip() if volume else "N/A"

            # output
            file.write(f"{ticker_text} {change_text} {volume_text}\n")
        # insert line break after every target site
        file .write("\n")

# get the trending headlines
with open("output.txt", "a") as file:
    file.write("https://finance.yahoo.com/topic/stock-market-news/\n")
    driver.get("https://finance.yahoo.com/topic/stock-market-news/")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all("section", class_=re.compile(r"container.*yf-"))

    # Loop through each title and print relevant info
    for section in sections:
        headline = section.find('h3', class_=re.compile(r"clamp.*yf-"))
        if headline:
            headline_text = headline.text.strip()
            file.write(f"{headline_text}\n")



# close web driver
driver.quit()

