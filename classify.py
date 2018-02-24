import pickle
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score
from instance import *
from location import *
import numpy as np


def main():
    with open('data/I_instances.pkl','rb') as f:
        instances = np.asarray(pickle.load(f))
    with open('data/cryptocurrencies_list.json') as f:
        cryptocurrencies = json.load(f)
    with open('data/cryptocurrency_abbreviations_list.json') as f:
        cryptocurrency_abbreviations = json.load(f)

    whitelist = [word.lower() for word in cryptocurrencies[:25] + cryptocurrency_abbreviations[:25]]

    indices_train, indices_test = train_test_split(np.asarray(range(len(instances))), test_size=0.33, random_state=42)
    X_train = np.asarray([x.features for x in instances[indices_train]])
    X_test= np.asarray([x.features for x in instances[indices_test]])
    y_train = np.asarray([y.label for y in instances[indices_train]])
    y_test = np.asarray([y.label for y in instances[indices_test]])

    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    
    # Any exact matches between our whitelist and the instance's word.
    y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances[indices_test]]
    predicted = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]
    accuracy = accuracy_score(y_test, predicted)
    precision = precision_score(y_test, predicted)
    recall = recall_score(y_test, predicted)
    f1 = 2*precision*recall/(precision+recall)

    print('\n\nDebugging:')		
    for i in range(len(predicted)):
        if predicted[i] != y_test[i] and y_test[i] == 0:
            print("predicted: {}, actual: {}, instance: {}".format(predicted[i], y_test[i], instances[indices_test][i]))


    for i in range(len(predicted)):
        if predicted[i] != y_test[i] and y_test[i] != 0:
            print("predicted: {}, actual: {}, instance: {}".format(predicted[i], y_test[i], instances[indices_test][i]))


    print('classifier accuracy: %f, precision: %f, recall: %f, f1: %f' % (accuracy, precision, recall, f1))		


if __name__ == '__main__':
    main()
    