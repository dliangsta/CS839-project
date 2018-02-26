import pickle
import json
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score
from instance import *
from location import *
import numpy as np

class Classifier:

    def __init__(self, clf_type, whitelist_path='data/whitelist.pkl', debug=False):
        self.clf_type = clf_type
        with open(whitelist_path,'rb') as f:
            self.whitelist = pickle.load(f)
        self.debug = debug

        if clf_type == 'dt':
            self.clf = DecisionTreeClassifier(random_state=0)
            self.clf_name = 'Decision Tree'
        elif clf_type == 'rf':
            self.clf = RandomForestClassifier(random_state=0)
            self.clf_name = 'Random Forest'
        elif clf_type == 'svm':
            self.clf = SVC()
            self.clf_name = 'Support Vector Machine'
        elif clf_type == 'lir':
            self.clf = LinearRegression()
            self.clf_name = 'Linear Regression'
        elif clf_type == 'lor':
            self.clf = LogisticRegression()
            self.clf_name = 'Logistic Regression'

    def classify(self, instances, train_indices=None, test_indices=None):
        if train_indices is None and test_indices is None and len(instances) > 1:
            # Partition set into train and test sets.
            train_indices, test_indices = train_test_split(np.asarray(range(len(instances))), test_size=0.33, random_state=42)
        elif (train_indices is None) ^ (test_indices is None):
            raise ValueError('Either provide both train_indices and test_indices or neither.')

        X_train = np.asarray([x.features for x in instances[train_indices]])
        X_test= np.asarray([x.features for x in instances[test_indices]])
        y_train = np.asarray([y.label for y in instances[train_indices]])
        y_test = np.asarray([y.label for y in instances[test_indices]])

        # Fit model.
        self.clf.fit(X_train, y_train)

        # Predict using model.
        y_predict = self.clf.predict(X_test)
        
        # Any exact matches between our whitelist and the instance's word.
        y_whitelist = [int(any([white == instance.stripped_lowered_word for white in self.whitelist])) for instance in instances[test_indices]]

        # results are those that are either whitelisted or predicted by the classfier.
        results = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]

        # Statistics
        accuracy = accuracy_score(y_test, results)
        precision = precision_score(y_test, results)
        recall = recall_score(y_test, results)
        try:
            f1 = 2*precision*recall/(precision+recall)
        except:
            f1 = -1.

        if self.debug:
            print('\n\nDebugging:')	
            print('\nFalse positives:')	
            # Print false positives.
            for i in range(len(results)):
                if results[i] != y_test[i] and y_test[i] == 0:
                    print("predicted: {}, actual: {}, instance: {}".format(results[i], y_test[i], instances[test_indices][i]))

            print('\nFalse negatives')
            # Print false negatives.
            for i in range(len(results)):
                if results[i] != y_test[i] and y_test[i] != 0:
                    print("predicted: {}, actual: {}, instance: {}".format(results[i], y_test[i], instances[test_indices][i]))
        
        print('%s accuracy: %f, precision: %f, recall: %f, f1: %f' % (self.clf_name, accuracy, precision, recall, f1))
        
        return accuracy, precision, recall, f1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='debug flag')
    parser.add_argument('--whitelist_path', default='data/whitelist.pkl', help='path for whitelist')
    args = parser.parse_args()
    print(args)
    with open('data/I_instances.pkl','rb') as f:
        instances = np.asarray(pickle.load(f))
    with open('data/cryptocurrencies_list.json') as f:
        cryptocurrencies = json.load(f)
    with open('data/cryptocurrency_abbreviations_list.json') as f:
        cryptocurrency_abbreviations = json.load(f)

    whitelist = [word.lower() for word in cryptocurrencies[:25] + cryptocurrency_abbreviations[:25]]
    clf = Classifier('dt', whitelist_path=args.whitelist_path, debug=args.debug)
    clf.classify(instances)

if __name__ == '__main__':
    main()
