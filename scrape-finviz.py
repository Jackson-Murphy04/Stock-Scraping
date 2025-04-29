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
options.add_argument("--headless")  # Enable headless mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
# init chrome driver
driver = webdriver.Chrome(options=options, service=service)

# scrape home page tickers, change, volume, and signal
with open("outData.txt", "a") as file:
    file.write("https://finviz.com/\n")
    driver.get("https://finviz.com/")
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # find all main page tickers
    titles = soup.find_all("tr", class_="styled-row")
    # Loop through each title and print relevant info
    for title in titles[:38]:
        # get and output info
        tds = title.find_all("td", align="right")
        ticker = title.find("a", class_="tab-link")
        change = title.find("span", class_="color-text is-positive")
        volume = tds[2]
        signal = title.find("a", class_="tab-link-nw")

        ticker_text = ticker.text.strip() if ticker else "N/A"
        change_text = change.text.strip() if change else "N/A"
        volume_text = volume.text.strip() if volume else "N/A"
        signal_text = signal.text.strip() if signal else "N/A"
        file.write(f"{ticker_text} {change_text} {volume_text} {signal_text}\n")
    file.write("\n")

# scrape news headlines
with open("outHeadlines.txt", "a") as file:
    file.write("https://finviz.com/news.ashx\n")
    driver.get("https://finviz.com/news.ashx")
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # find all headlines
    titles = soup.find_all("td", class_="news_link-cell")
    for title in titles:
        # get and output info
        headline = title.find("a")
        headline_text = headline.text.strip() if headline else "N/A"
        file.write(f"{headline_text}\n")
    file.write("\n")

# scrape insider trades
with open("outData.txt", "a") as file:
    file.write("https://finviz.com/insidertrading.ashx\n")
    driver.get("https://finviz.com/insidertrading.ashx")
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # find all headlines
    titles = soup.find_all("tr", class_="fv-insider-row")
    for title in titles:
        # Skip rows with the specific class
        if "is-option" in title.get("class", []) and "bg-white" in title.get("class", []):
            continue
        # get and output info
        tds = title.find_all("td", class_="text-right")
        ticker = title.find("a", class_="tab-link")
        trans = title.find("td", class_="whitespace-nowrap text-center")
        amount = tds[2]

        ticker_text = ticker.text.strip() if ticker else "N/A"
        trans_text = trans.text.strip() if trans else "N/A"
        amount_text = amount.text.strip() if amount else "N/A"
        file.write(f"{ticker_text} {trans_text} {amount_text}\n")
    file.write("\n")

driver.close()