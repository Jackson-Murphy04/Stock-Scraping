import json
import string
import re
from collections import defaultdict
from collections import Counter
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# input files
nasdaq_file = "nasdaq.json"
nyse_file = "nyse.json"

# load data
def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

nasdaq_data = load_json_file(nasdaq_file)
nyse_data = load_json_file(nyse_file)
combined_data = nasdaq_data + nyse_data

# Clean text function to remove punctuation and trailing suffixes
def clean_text(name):
    name = name.lower()
    name = name.translate(str.maketrans('', '', string.punctuation))

    suffixes = [
        "common stock", "preferred stock",
        "class a", "class b", "class a common stock", "class b common stock",
        "american depositary shares", "depositary shares",
        "ordinary shares", "class a ordinary shares", "class b ordinary shares",
        "units", "warrant", "warrants", "rights"
    ]

    for suffix in sorted(suffixes, key=len, reverse=True):
        if name.endswith(suffix):
            name = name[: -len(suffix)].strip()

    name = " ".join(name.split())  # remove extra spaces
    return name

# build dict
ticker_to_name = {}
name_to_ticker = {}
keyword_to_tickers = defaultdict(list)

for entry in combined_data:
    ticker = entry.get("symbol", "").upper()
    name = entry.get("name", "").strip()
    if not ticker or not name:
        continue

    if '^' in ticker:
        continue

    if '/' in ticker:
        continue

    name_clean = clean_text(name)
    ticker_to_name[ticker] = name_clean
    name_to_ticker[name_clean] = ticker

    # Split into keywords and strip commas/punctuation
    for word in name_clean.split():
        keyword_to_tickers[word].append(ticker)

# read in headlines
headlines = []
with open("outHeadlines.txt","r") as input:
    for line in input:
        line = line.strip().lower()
        if line[:5] != "https":
            if line:
                headlines.append(line)

# list of generic words to skip
STOPWORDS = {
    "the", "of", "in", "at", "this", "that", "but", "on", "and", "for", "to", "with", "a", "an",
    "by", "from", "as", "if", "so", "when", "then", "its", "into", "about", "over", "out", "off",
    "price", "value", "gain", "loss", "rise", "fall", "plenty", "market", "stock", "shares", "top", 
    "are", "now", "five", "rare", "see", "low", "buy", "best",
    # Industry-Specific
    "Technologies", "Pharmaceuticals", "Healthcare", "Industries", "Energy",
    "Mining", "Software", "Biotech", "Biosciences", "Telecom", "Financial",
    "Insurance", "Retail", "Logistics", "Holdings",

    # Business Structure
    "Corporation", "Corp", "Incorporated", "Inc", "Company", "Co", "Limited",
    "Ltd", "Group", "Partners", "Partnership", "Enterprises", "Associates", "LLC",

    # Common Naming Words
    "Global", "International", "National", "American", "United", "First",
    "Capital", "Systems", "Solutions", "Resources", "Services", "Network", "Trust",

    # Geographic References
    "America", "American", "Pacific", "Atlantic", "Western", "Southern",
    "Northern", "Eastern", "Central",

    # Finance & Real Estate
    "Bank", "Trust", "Capital", "Realty", "Investments", "Mortgage", "Equity"
}

matches = {}
min_hits = 1
for headline in headlines:
    tick = []  # Initialize tick list once per headline
    # Clean the headline
    translator = str.maketrans('', '', string.punctuation)
    words = headline.translate(translator).lower().split()

    ticker_hits = Counter()

    for word in words:
        if len(word) < 3 or word in STOPWORDS:
            continue

        matched_tickers = keyword_to_tickers.get(word)
        if matched_tickers:
            ticker_hits.update(matched_tickers)

    # Only return tickers with strong enough signal
    filter = [ticker for ticker, count in ticker_hits.items() if count >= min_hits]
    tick.extend(filter)
    # Remove duplicates and store in matches as long as not too many
    if len(tick) <= 5 and len(tick) > 0:
        matches[headline] = list(tick)
        #print(headline, matches[headline])

# init sentiment analyzer
sia = SentimentIntensityAnalyzer()

scores = {}
# run sentiment on matches list 
for headline in headlines:
    score = sia.polarity_scores(headline)
    #scores.append(score['compound'])
    scores[headline] = score['compound']

# sort
scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

# match known data in matches to scores in sorted
final = []
for line in matches:
    final.append([line,matches[line], scores[line]])

# score all tickers, sort, and output
tick_scores = {}
for line in matches:
    tickers = matches[line]
    score = scores[line]
    for ticker in tickers:
        if ticker in tick_scores:
            tick_scores[ticker] += score
        else:
            tick_scores[ticker] = score

# use other scraped trading data to alter scores
data = []
# we loop the scraped data file line by line and skip https or empty lines and add the rest to a list
with open('outData.txt', 'r') as input:
        for line in input:
            line = line.strip()
            if line[:5] != 'https':
                if line:
                    data.append(line)

# score data points 
#scores = {}
for point in data:
    match = re.search(r'([-+]?\d+\.\d+)%', point)
    if match:
        percent = float(match.group(1))
        tick_scores[point.split()[0]] = (percent / 1000) 
    if point.split()[1] == "Buy":
        if point.split()[0] in tick_scores:
            tick_scores[point.split()[0]] += 0.2
        else:
            tick_scores[point.split()[0]] = 0.2
# sort by highest scores
tick_scores = dict(sorted(tick_scores.items(), key=lambda item: float(item[1]), reverse=True))

# sort and output all scores
with open("finalOut.txt", "w") as file:
    for tick in tick_scores:
        file.write(f"{tick}: {tick_scores[tick]}\n")
        # ideally find way to output all headlines associated with ticker and score

# Print only the first 5 tickers and their scores
for i, tick in enumerate(tick_scores):
    if i >= 5: 
        break
    print(tick, tick_scores[tick])