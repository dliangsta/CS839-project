import pickle
import json
from instance import *
from location import *

def main():
    instances = []
    # Iterate over all documents.

    with open('data/prune_list.json') as f:
        prune_list = json.load(f)

    one_count = 0
    zero_count = 0
    for i in range(1,331):
        with open('data/labeled/' + str(i)) as f:
            data = [line.strip() for line in f.readlines()]

            # Iterate over lines in document.
            for j, labeled_line in enumerate(data):
                original_line = data[j-1]

                # Skip every other line, because we handle the lines in pairs.
                if j % 2 == 1: 

                    # Iterate over each character in the line to find each word.
                    k = 0
                    while k < len(labeled_line):
                        label = 1 if labeled_line[k] == '1' else 0
                        # Index of end of label.
                        l = labeled_line.find(' ', k)
                        if l < k:
                            break


                        word = original_line[k:l]
                        if len(word) and any([c.isalpha() for c in word]):
                            if not shouldPruneWord(word, prune_list):
                                if label == 1:
                                    one_count += 1
                                else:
                                    zero_count += 1
                                # Make features.
                                features = []
                                features.append(hasAllCaps(word))
                                features.append(surroundedByParentheses(word))
                                features.append(wordLength(word))
                                features.append(firstLetterCapitalized(word))
                                features.append(containsCashSubstring(word))
                                features.append(containsCoinSubstring(word))
                                features.append(numCapitals(word))

                                location = Location(i, j, k)
                                instance = Instance(location=location, 
                                                    label=label, 
                                                    word=word,
                                                    features=features)
                                instances.append(instance)

                                print(instance)
                        k = l+1

    print(one_count, zero_count)
    # Save dataset.
    with open('data/instances.pkl','wb') as f:
        pickle.dump(instances, f)

def shouldPruneWord(word, prune_list):
    word = removePunctuation(word)
    return word in prune_list

# Features
def hasAllCaps(word):
    word = removePunctuation(word)
    return int(word.upper() == word)

def surroundedByParentheses(word):
    # Remove leading and trailing quotations
    word = removePunctuation(word)
    return int(word[0] == '(' and word[-1] == ')')

def wordLength(word):
	word = removePunctuation(word)
	return len(word)

def firstLetterCapitalized(word):
	word = removePunctuation(word)
	return int(word[0].isupper())

def containsCashSubstring(word):
    # Determines if any of these key words are substrings.
    return int('cash' in word.lower())

def containsCoinSubstring(word):
    return int('coin' in word.lower())

def numCapitals(word):
    word = removePunctuation(word)
    return sum(1 for c in word if c.isupper() and c.isalpha())

# Utilities
def removePunctuation(word):
    punctuation = ['\'','"','.','?','!',',',';',':']
    while len(word) and word[0] in punctuation:
        word = word[1:]
    while len(word) and word[-1] in punctuation:
        word = word[:-1]
    return word



if __name__ == '__main__':
    main()