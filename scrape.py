import datetime
from dateutil.relativedelta import relativedelta
from eventregistry import *

out = ''
er = EventRegistry(apiKey = 'c4e1c037-d70b-4c75-a11e-b98809a5fc47')
for i in range(5):
    q = QueryArticlesIter(keywords=QueryItems.AND(['cryptocurrency','$','price']), 
                        dateStart=(datetime.datetime.now().replace(day=1) - relativedelta(months=i+1)), 
                        dateEnd=(datetime.datetime.now().replace(day=1) - relativedelta(months=i)),
                        lang='eng')
    results = q.execQuery(er, sortBy = 'date', maxItems=10)
    for article in results:
        out += str(article) + '\n'
    print(out)
    print(i)

with open('articles.txt','w') as f:
    f.write(out)
