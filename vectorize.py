import pickle
from instance import *
from location import *

def main():
    instances = []
    for a in range(1,331):
        with open('data/labeled/' + str(a)) as f:
            data = [line.strip() for line in f.readlines()]
            for i, labeled_line in enumerate(data):
                original_line = data[i-1]
                if i % 2 == 1:
                    for j in range(len(labeled_line)):
                        if labeled_line[j] == '1':
                            k = labeled_line.find(' ',j)
                            label = labeled_line[j:k]
                            word = original_line[j:k]
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
                            print(features)


                            location = Location(i, j)
                            instance = Instance(location=location, 
                                                label=1, 
                                                features=features)
                            instances.append(instance)

    with open('data/instances.pkl','wb') as f:
        pickle.dump(instances, f)


def hasAllCaps(word):
    word = removePunctuation(word)
    return int(word.upper() == word)

def surroundedByParentheses(word):
    # Remove leading and trailing quotations
    word = removePunctuation(word)
    return int(word[0] == '(' and word[-1] == ')')

def containsCashSubstring(word):
    # Determines if any of these key words are substrings.
    return int('cash' in word.lower())

def containsCoinSubstring(word):
    return int('coin' in word.lower())


def wordLength(word):
	word = removePunctuation(word)
	return len(word)

def firstLetterCapitalized(word):
	word = removePunctuation(word)
	return int(word[0].isupper())

def removePunctuation(word):
    punctuation = ['\'','"','.','?','!',',',';',':']
    while word[0] in punctuation:
        word = word[1:]
    while word[-1] in punctuation:
        word = word[:-1]
    return word



if __name__ == '__main__':
    main()