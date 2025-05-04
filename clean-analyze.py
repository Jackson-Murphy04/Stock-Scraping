import json
import string
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
    "are", "now", "five", "rare", "see", "low"
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
sorted = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

# match known data in matches to scores in sorted
final = []
for line in matches:
    final.append([line,matches[line], scores[line]])
    print(line, matches[line], scores[line])

