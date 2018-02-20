import json
import random
import numpy as np

DIRECTORY = 'data/'
NAMES = ['aishwarya','david','vish']

def main():
    with open(DIRECTORY + 'raw.json') as f:
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

    counter = 1
    for i in range(len(NAMES)): 
        indices = range(i,len(selected_articles),len(NAMES))
        partition = selected_articles[indices]
        for article in partition:
            with open(DIRECTORY + 'documents/' + str(counter),'w') as f:
                json.dump(article, f)
                counter += 1
        with open(DIRECTORY + NAMES[i] + '_raw.json', 'w') as f:
            json.dump(partition.tolist(), f)

        print(len(partition))
        
if __name__ == '__main__':
    main()
    