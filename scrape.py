import datetime
import json
from dateutil.relativedelta import relativedelta
from eventregistry import *

def main():
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

if __name__ == '__main__':
    main()
    