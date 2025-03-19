import requests
from bs4 import BeautifulSoup
import time

# URL of the target site
url = "https://finance.yahoo.com/markets/stocks/trending/"

# Custom headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Fetch the page content using requests with custom headers
response = requests.get(url, headers=headers)
html = response.text

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all 'tr' elements with class 'row false yf-hhhli1' which contain the trending stocks and info
titles = soup.find_all("tr", class_="row false yf-hhhli1")

# Loop through each title and print relevant info
for title in titles:
    # Find the ticker symbol of each the % change and the volume 
    ticker = title.find('span', class_="symbol yf-1fqyif7")
    print(ticker.text)