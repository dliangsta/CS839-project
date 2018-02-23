import json
import os

with open ('data/duplicate_documents.json') as f:
    data = json.load(f)

for i in data:
    os.remove('data/labeled/'+str(i+1))
    os.remove('data/unlabeled/'+str(i+1))