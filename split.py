import json

def main():
    with open('data/raw.json') as f:
        data = json.load(f)
        print(len(data))
    for i, article in enumerate(data):
        if i < 330:
            with open('data/unlabeled/' + str(i+1), 'w') as ff:
                json.dump(article, ff)
        
if __name__ == '__main__':
    main()