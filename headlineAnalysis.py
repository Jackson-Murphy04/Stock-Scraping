import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# init sentiment analyzer
sia = SentimentIntensityAnalyzer()

headlines = []
# then we loop the scraped data file line by line and run sentiment analysis on the headlines
with open('outHeadlines.txt', 'r') as input:
        for line in input:
            line = line.strip()
            if line[:5] != 'https':
                if line:
                    headlines.append(line)

scores = []

# VADER scoring
for headline in headlines:
    score = sia.polarity_scores(headline)
    scores.append(score['compound'])
