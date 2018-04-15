import pickle
import json

def main():
    with open('data/cryptocurrencies_list.json') as f:
        cryptocurrencies = json.load(f)
    with open('data/cryptocurrency_abbreviations_list.json') as f:
        cryptocurrency_abbreviations = json.load(f)

    whitelist = [word.lower() for word in cryptocurrencies[:25] + cryptocurrency_abbreviations[:25]]

    with open('data/whitelist.pkl','wb') as f:
        pickle.dump(whitelist, f)

if __name__ == '__main__':
    main()