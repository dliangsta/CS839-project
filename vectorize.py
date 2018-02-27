import pickle
import json
import string
import numpy as np
from instance import *
from location import *

class Vectorizer:
    def __init__(self, prune_list=None, cryptocurrencies=None):
        self.one_count = 0
        self.zero_count = 0
        self.prune_list = prune_list
        self.cryptocurrencies = [cryptocurrency.lower() for cryptocurrency in cryptocurrencies]
        self.instances = []

    def vectorize(self, docs):
        for i in docs:
            with open('data/labeled/' + str(i), encoding='utf8') as f:
                data = [line.strip() for line in f.readlines()]

                # Iterate over lines in document.
                for j, labeled_line in enumerate(data):
                    original_line = data[j-1]
                    if j < len(data) - 2: # send next line in case we need first word(s) of next line
                        original_next = data[j+1]
                        labeled_next = data[j+2]
                        k_n = 0
                        l_n = labeled_next.find(' ', k_n)
                        next_line_word1 = original_next[k_n:l_n] # first word of next line
                        k_n = l_n + 1
                        l_n = labeled_next.find(' ', k_n)
                        next_line_word2 = original_next[k_n:l_n] # second word of next line
                    else:
                        next_line_word1 = '' # last line, last word won't have a next word(s)
                        next_line_word2 = ''

                    # Skip every other line, because we handle the lines in pairs.
                    if j % 2 == 1: 
                        self.vectorize_line(i, j, original_line, labeled_line, next_line_word1, next_line_word2)
        return self.instances

    def vectorize_line(self, i, j, original_line, labeled_line, next_line_word1, next_line_word2):
        # Iterate over each character in the line to find each word.
        k = 0
        while k < len(labeled_line):
            label = 1 if labeled_line[k] != '`' else 0
            # Index of end of label.
            l = labeled_line.find(' ', k)

            # If cannot be found, l will be -1 so we are at the end of the line.
            if l < k:
                break
            word = original_line[k:l]

            # Find next word
            k_n = l+1
            l_n = labeled_line.find(' ', k_n)

            if l_n > k_n: # found next word
                next_word = original_line[k_n:l_n]
                eol = False # not end of line
            else:
                next_word = next_line_word1 # last word of line won't have following word, so we've passed it in
                eol = True # end of line

            # Find next-next word
            if not eol:
                k_n = l_n+1
                l_n = labeled_line.find(' ', k_n)

                if l_n > k_n: # found next next word
                    next_next_word = original_line[k_n:l_n]
                else:
                    next_next_word = next_line_word1 # first word of next line will be third word in this sequence
            else:
                next_next_word = next_line_word2 # next word was found on following line, so next-next word will be one after

            words = [word, ' '.join([word, next_word])] if next_word else [word] # if there isn't a next word don't want to repeat same word twice
            next_words = [next_word, next_next_word]

            for idx, word in enumerate(words):
                if len(word) and any([c.isalpha() for c in word]):
                    if not self.shouldPruneWord(word):
                        # Make features.
                        feature_functions = [self.hasAllCaps,
                                            self.isSurroundedByParentheses,
                                            self.wordLength,
                                            self.numCapitals,
                                            self.firstLetterCapitalized,
                                            self.containsCashSubstring,
                                            self.containsCoinSubstring,
                                            self.containsTokenSubstring,
                                            self.containsForwardSlash,
                                            self.containsDash,
                                            self.containsApostrophe,
                                            self.containsDot,
                                            self.containsComma,
                                            self.containsMoneySign,
                                            self.containsPound,
                                            self.containsPlus,
                                            self.containsIumSubstring,
                                            self.containsEumSubstring,
                                            #self.inCryptocurrenciesList
                                            ] 
                        features = [func(word) for func in feature_functions] + self.alphabetCounts(next_words[idx]) #+ self.charCounts(word)

                        location = Location(i, j, k, l)
                        instance = Instance(location=location, 
                                            label=label, 
                                            word=word,
                                            features=features)

                        self.instances.append(instance)
                        if label == 1:
                            self.one_count += 1
                        else:
                            self.zero_count += 1
            k = l+1

    def shouldPruneWord(self, word):
        word = removePunctuation(word)
        return word in self.prune_list

    # Features
    def hasAllCaps(self, word):
        word = removePunctuation(word)
        return int(word.upper() == word)

    def isSurroundedByParentheses(self, word):
        word = removePunctuation(word)
        return int(word[0] == '(' and word[-1] == ')')

    def inCryptocurrenciesList(self, word):
        word = removePunctuation(word)
        return int(word.lower() in self.cryptocurrencies)

    def wordLength(self, word):
        word = removePunctuation(word)
        return len(word)

    def numCapitals(self, word):
        word = removePunctuation(word)
        return sum(1 for c in word if c.isupper() and c.isalpha())

    def firstLetterCapitalized(self, word):
        word = removePunctuation(word)
        return int(word[0].isupper())

    def containsCashSubstring(self, word):
        return int('cash' in word.lower())

    def containsCoinSubstring(self, word):
        return int('coin' in word.lower())

    def containsTokenSubstring(self, word):
        return int ('token' in word.lower())

    def containsEumSubstring(self, word):
        return int('eum' in word.lower())

    def containsIumSubstring(self, word):
        return int('ium' in word.lower())

    def containsForwardSlash(self, word):
        return int('/' in word)

    def containsDash(self, word):
        return int('-' in word)

    def containsApostrophe(self, word):
        return int('\'' in word)

    def containsDot(self, word):
        return int('.' in word)

    def containsComma(self, word):
        return int(',' in word)

    def containsMoneySign(self, word):
        return int('$' in word)

    def containsPound(self, word):
        return int('#' in word)

    def containsPlus(self, word):
        return int('+' in word)


    def charCounts(self, word):
        return [word.count(chr(letter)) for letter in range(128)]

    def alphabetCounts(self, word):
        lower = word.lower()
        return [lower.count(chr(letter)) for letter in range(97, 123)]



def main():
    # Iterate over all documents.

    with open('data/prune_list.json') as f:
        prune_list = json.load(f)
    with open('data/cryptocurrencies_list.json') as f:
        cryptocurrencies = json.load(f)

    docs = list(range(1, 301))

    v = Vectorizer(prune_list, cryptocurrencies)

    instances = v.vectorize(docs)
    # for instance in instances:
    #     print(instance)

    np.random.seed(0)
    np.random.shuffle(docs)
    I_size = int(len(docs) * (2.0/3))
    J_size = len(docs) - I_size
    I_docs = docs[:I_size]
    J_docs = docs[I_size:]


    I_instances = []
    J_instances = []

    for instance in instances:
        if instance.location.doc_num in I_docs:
            I_instances.append(instance)
        elif instance.location.doc_num in J_docs:
            J_instances.append(instance)

    print(len(docs), I_size, J_size, len(I_docs), len(J_docs), len(I_instances), len(J_instances))
    print(v.one_count, v.zero_count)

    # Save dataset.
    with open('data/I_instances.pkl','wb') as f:
        pickle.dump(I_instances, f)
    with open('data/J_instances.pkl','wb') as f:
    	pickle.dump(J_instances, f)
    with open('data/I_docs.json','w') as f:
        json.dump(I_docs, f)
    with open('data/J_docs.json','w') as f:
        json.dump(J_docs, f)

# Utilities
def removePunctuation(word):
    punctuation = ['\'','"','.','?','!',',',';',':','[',']']
    while len(word) and word[0] in punctuation:
        word = word[1:]
    while len(word) and word[-1] in punctuation:
        word = word[:-1]
    return word



if __name__ == '__main__':
    main()