# read in headlines
headlines = []
with open("outHeadlines.txt","r") as input:
    for line in input:
        line = line.strip()
        if line[:5] != "https":
            if line:
                headlines.append(line)

#read in tickers from data file
tickers = []
with open("outData.txt", "r") as input:
    for line in input:
        if line[:5] != "https":
            parts = line.strip().split()
            if parts:
                ticker = parts[0].strip().lower()
                tickers.append(ticker)

# check if headline matches to a ticker
matches = []
for headline in headlines:
    headline_lower = headline.lower()
    matched_stock = []
    for ticker in tickers:
        if ticker in headline_lower:
            matched_stock.append(ticker)
            matches.append((headline,matched_stock))


