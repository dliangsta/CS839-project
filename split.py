import json

def main():
    with open('data/raw.json') as f:
        data = json.load(f)
        print(data)
    for i, article in enumerate(data):
        print(i)
        with open('data/documents/' + str(i), 'w') as ff:
            json.dump(article, ff)
        
if __name__ == '__main__':
    main()