import pickle
from instance import *
from location import *

def main():
    instances = []
    for i in range(1,331):
        with open('data/labeled/' + str(i)) as f:
            data = [line.strip() for line in f.readlines()]
            for j, labeled_line in enumerate(data):
                original_line = data[j-1]
                if j % 2 == 1:
                    for k in range(len(labeled_line)):
                        if labeled_line[k] == '1':
                            l = labeled_line.find(' ',k)
                            label = labeled_line[k:l]
                            word = original_line[k:l]
                            print(label)
                            print(word)
                            # Make features
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
                                                label=1, 
                                                features=features)
                            instances.append(instance)

                            print(instance)
                            
    with open('data/instances.pkl','wb') as f:
        pickle.dump(instances, f)

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
    while word[0] in punctuation:
        word = word[1:]
    while word[-1] in punctuation:
        word = word[:-1]
    return word



if __name__ == '__main__':
    main()