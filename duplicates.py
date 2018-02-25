import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

data = []
for i in range(1,361):
    try:
        with open('data/unlabeled/'+str(i)) as f:
            data.append(json.load(f))
    except:
        pass

S = []
remove = []
for i, article in enumerate(data):
    for j, article2 in enumerate(data):
        if j > i and j not in remove and i not in remove:
            s = similar(article, article2)
            if s > .5:
                remove.append(j)
                print(i,j,s)
                S.append(s)

with open ('data/duplicate_documents.json') as f:
    json.dump(remove, f)
    
print(remove)   