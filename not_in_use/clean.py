import yfinance as yf
import re
# get company name of each ticker to compare with headlines
def get_company_name(ticker):
    try:
        stock = yf.Ticker(ticker)
        name = stock.info.get('shortName') or stock.info.get('longName')
        if name:
            return name.lower()
    except:
        return None

# read in headlines
headlines = []
with open("outHeadlines.txt","r") as input:
    for line in input:
        line = line.strip()
        if line[:5] != "https":
            if line:
                headlines.append(line)

# read in tickers from data file
tickers = []
with open("outData.txt", "r") as input:
    for line in input:
        if line[:5] != "https":
            parts = line.strip().split()
            if parts:
                ticker = parts[0].strip().lower()
                tickers.append(ticker)

# convert tickers to company name
ticker_to_name = {}
for ticker in tickers:
    name = get_company_name(ticker)
    if name:
        ticker_to_name[ticker] = name


# exclude generic words found in many company names
EXCLUDE = {
    "inc", "co", "corp", "group", "company", "stock", "capital",
    "holdings", "markets", "limited", "ltd", "llc", "plc", "fund",
    "technologies", "global", "international"
}
with open("matches.txt", "a") as output_file:
    for headline in headlines:
        headline_lower = headline.lower()
        matched_ticker = None

        # check if headline contains a ticker first
        ticker_match = re.search(r'\(([A-Z]{1,5})\)', headline)
        if ticker_match:
            candidate = ticker_match.group(1).lower()
            if candidate in tickers:
                matched_ticker = candidate

        # if no ticker, check for a company name
        if not matched_ticker:
            for ticker, full_name in ticker_to_name.items():
                name_parts = re.findall(r'\w+', full_name)
                if not name_parts:
                    continue
                first_word = name_parts[0].lower()
                if len(first_word) <= 3 or first_word in EXCLUDE:
                    continue
                if re.search(rf'\b{re.escape(first_word)}\b', headline_lower):
                    matched_ticker = ticker
                    break

        if matched_ticker:
            output_file.write(f"[{matched_ticker}] {headline.strip()}\n")
