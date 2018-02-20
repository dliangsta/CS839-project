import json

data = []
for i in range(1,331):
    with open('data/unlabeled/'+str(i)) as f:
        data.append(json.load(f))

seen = set()
uniq = [x for x in data if x not in seen and not seen.add(x)]  
print(len(uniq))
print(len(data))