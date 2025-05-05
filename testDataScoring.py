import re

data = []
# we loop the scraped data file line by line and skip https or empty lines and add the rest to a list
with open('outData.txt', 'r') as input:
        for line in input:
            line = line.strip()
            if line[:5] != 'https':
                if line:
                    data.append(line)

# score data points 
scores = {}
for point in data:
    match = re.search(r'([-+]?\d+\.\d+)%', point)
    if match:
        percent = float(match.group(1))
        scores[point.split()[0]] = (percent / 1000) 
    if point.split()[1] == "Buy":
        if point.split()[0] in scores:
            scores[point.split()[0]] += 0.2
        else:
            scores[point.split()[0]] = 0.2
# sort by highest scores
scores = dict(sorted(scores.items(), key=lambda item: float(item[1]), reverse=True))

# output ticker and score
for score in scores:
    print(score, scores[score])