import datetime
from dateutil.relativedelta import relativedelta
from eventregistry import *

def main():
    er = EventRegistry(apiKey = 'c4e1c037-d70b-4c75-a11e-b98809a5fc47')

    q = QueryArticlesIter(keywords=QueryItems.AND(['cryptocurrency','$','price']), 
                        lang='eng')
                        
    results = q.execQuery(er, sortBy = 'date', maxItems=1000)
    data = [article['body'] for article in results]
    print(data)

    with open('data/raw.json','w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    main()
    