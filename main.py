import datetime
import json
from dateutil.relativedelta import relativedelta
from eventregistry import *

CRYPTO = '1'
UNSURE = '`'

def main():
    # scrape()
    split()
    prepare()

def scrape():
    er = EventRegistry(apiKey = 'c4e1c037-d70b-4c75-a11e-b98809a5fc47')

    q = QueryArticlesIter(keywords=QueryItems.AND(['cryptocurrency','$','price']), 
                        lang='eng')
                        
    # Note, the results are not the same every time.
    results = q.execQuery(er, sortBy = 'date', maxItems=1000)

    text = []
    for article in results:
        # Results are not guaranteed to be unique.
        if article['body'] not in text:
            text.append(article['body'])
    print(text)

    with open('data/raw.json','w') as f:
        json.dump(text, f)

def split():
    with open('data/raw.json') as f:
        data = json.load(f)
        print(len(data))
    for i, article in enumerate(data):
        if i < 330:
            with open('data/unlabeled/' + str(i+1), 'w') as ff:
                json.dump(article, ff)
def prepare():
    with open('data/cryptocurrencies_list.json') as f:
        # Take top n currencies.
        n = 100
        cryptocurrencies = [cryptocurrency_name.lower() for cryptocurrency_name in json.load(f)[:n]]

    for i in range(1,331):
        with open('data/unlabeled/' + str(i)) as f:
            article = json.load(f) 


        out = ''
        # Clean article.
        article = article.replace('  ',' ').replace(' \n','\n').replace('\n ','\n').replace('\n\n','\n')
        # Split into lines.
        lines = article.split('\n')

        for line in lines:
            line = line.strip() + '.'
            if len(line) > 0:
                out += line + '\n'
                words = line.split(' ')

                for j, word in enumerate(words):
                    out_line = label(word, cryptocurrencies) + '_' * (len(words[j])-1) + ' '
                    out += out_line

                out += '\n'

        out += '\n'

        with open('data/labeled/' + str(i),'w') as f:
            f.write(out)

# Manually label easy cases, like all occurrences of 'bitcoin'
def label(original_word, cryptocurrencies):
    # Remove some punctuation
    word = original_word.strip().replace('(','').replace(')','').replace('.','').replace('"','').replace(',','')
    # Some words like "Ripple's" won't be in our list
    word = re.split('\'', word)[0].lower()

    return CRYPTO if word in cryptocurrencies or word[:-1] in cryptocurrencies else UNSURE

if __name__ == '__main__':
    main()
    