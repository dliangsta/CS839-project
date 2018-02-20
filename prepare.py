import json
import re

CRYPTO = '1'
UNSURE = '`'

def main():

    directory = 'data/'
    names = ['aishwarya','david','vish']

    with open('data/cryptocurrencies_list.json') as f:
        # Take top n currencies.
        n = 10
        cryptocurrencies = [cryptocurrency_name.lower() for cryptocurrency_name in json.load(f)[:n]]

    # Manual exceptions.
    blacklist = []

    for name in names:
        
        with open(directory + name + '_raw.json') as f:
            data = json.load(f) 


        out = ''
        for article in data:
            # Clean article.
            article = article.replace('  ',' ').replace(' \n','\n').replace('\n ','\n').replace('\n\n','\n')
            # Split into lines.
            lines = article.split('\n')

            for line in lines:
                line = line.strip() + '.'
                if len(line) > 0:
                    out += line + '\n'
                    words = line.split(' ')

                    for i, word in enumerate(words):
                        out_line = label(cryptocurrencies, blacklist, word) + '_' * (len(words[i])-1) + ' '
                        out += out_line

                    out += '\n'

            out += '\n'

        # print(out)    
        with open(directory + name + '_prepared.txt','w') as f:
            f.write(out)

# Manually label easy cases, like all occurrences of 'bitcoin'
def label(cryptocurrencies, blacklist, original_word):
    # Remove some punctuation
    word = original_word.strip().replace('(','').replace(')','').replace('.','')
    # Some words like "Ripple's" won't be in our list
    word = re.split('\'', word)[0].lower()

    if word in cryptocurrencies and original_word not in blacklist:

        return CRYPTO

    return UNSURE
        

if __name__ == '__main__':
    main()

