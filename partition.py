import json
import random
import numpy as np

directory = 'data/'
names = ['aishwarya','david','vish']

with open(directory + 'raw.json') as f:
    data = json.load(f)

article_lengths = []
for article in data:
    article_lengths.append(len(article))

article_lengths.sort()
print(article_lengths)
print(np.mean(article_lengths))

# select shortest 330 articles
selected_articles = []
for article in data:
    if len(article) < article_lengths[330]:
        print(article)
        selected_articles.append(article)

selected_articles = np.array(selected_articles)

for i in range(len(names)): 
    indices = range(i,len(selected_articles),len(names))
    partition = selected_articles[indices]
    with open(directory + names[i] + '_raw.json', 'w') as f:
        json.dump(partition.tolist(), f)

    print(len(partition))
    