import datetime
import json
from dateutil.relativedelta import relativedelta
from eventregistry import *
from difflib import SequenceMatcher

CRYPTO = '1'
UNSURE = '`'
existing_docs = []
scraperound = 2

def main():
    if scraperound == 2:
        #load_existing_docs()
        #scrape_more()
        pass
    else:
        #scrape()
        pass
    split()
    prepare()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def load_existing_docs():
    for i in range(1,331):
        try:
            with open('data/unlabeled/'+str(i)) as f:
                existing_docs.append(json.load(f))
        except:
            pass

def is_existing_docs(current):
    for i, article in enumerate(existing_docs):
        s = similar(article, current)
        if s > .5:
            print ("Similar with " + str(i))
            return 1
    return 0

def scrape_more():
    count = 0
    text = []
    #looking for some new cryptocurrencies in round 2 to avoid skew due to popular ones!
    
    with open('data/lookfor.json') as f:
        lookforcryptocurrencies = [cryptocurrency_name.lower() for cryptocurrency_name in json.load(f)[:]]
    
    while count <40:
        for cryptocurrency in lookforcryptocurrencies:
            er = EventRegistry(apiKey = 'c4e1c037-d70b-4c75-a11e-b98809a5fc47')
            q = QueryArticlesIter(keywords=QueryItems.AND([cryptocurrency, 'cryptocurrency', 'price']), 
                                lang='eng')
            # Note, the results are not the same every time.
            results = q.execQuery(er, sortBy = 'date', maxItems=100)
            print (cryptocurrency)
            for article in results:
                # Results are not guaranteed to be unique. so we check existing docs for similarity
                if article['body'] not in text:
                    if cryptocurrency in str(article['body']).lower():
                        if is_existing_docs(article['body']) != 1:
                            text.append(article['body'])
                            existing_docs.append(article['body'])
                            print ("found " + cryptocurrency)
                            count += 1
                            break
            if count >= 40:
                break
            print (count)

    with open('data/raw2.json','w') as f:
        json.dump(text, f)
       
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
    filename = 'data/raw.json'
    offset = 1
    if scraperound == 2:
        filename = 'data/raw2.json'
        offset = 331
    with open(filename) as f:
        data = json.load(f)
        print(len(data))
    for i, article in enumerate(data):
        if i < 330:
            with open('data/unlabeled/' + str(i+offset), 'w') as ff:
                json.dump(article, ff)

def prepare():
    with open('data/cryptocurrencies_list.json') as f:
        # Take top n currencies.
        n = 100
        cryptocurrencies = [cryptocurrency_name.lower() for cryptocurrency_name in json.load(f)[:n]]
    '''   
    with open('data/lookfor.json') as f:
        cryptocurrencies.append([cryptocurrency_name.lower() for cryptocurrency_name in json.load(f)[:]])

    with open('data/cryptocurrency_abbreviations_list.json') as f:
        cryptocurrencies.append([cryptocurrency_name.lower() for cryptocurrency_name in json.load(f)[:10]])
    '''
    
    start = 1
    end = 331
    if scraperound == 2:
        start = 331
        end = 371
    
    for i in range(start, end):
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
    