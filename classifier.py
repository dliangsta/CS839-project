import pickle
import json
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

    def __init__(self, clf_type, debug=False):
        self.clf_type = clf_type
        self.debug = debug

        if clf_type == 'dt':
            self.clf = DecisionTreeClassifier(random_state=0)
        elif clf_type == 'rf':
            self.clf = RandomForestClassifier(random_state=0)
        elif clf_type == 'svm':
            self.clf = SVC()
        elif clf_type == 'lir':
            self.clf = LinearRegression()
        elif clf_type == 'lor':
            self.clf = LogisticRegression()

    def classify(self, instances, whitelist=None, blacklist=None):
        # Partition set into train and test sets.
        indices_train, indices_test = train_test_split(np.asarray(range(len(instances))), test_size=0.33, random_state=42)

        X_train = np.asarray([x.features for x in instances[indices_train]])
        X_test= np.asarray([x.features for x in instances[indices_test]])
        y_train = np.asarray([y.label for y in instances[indices_train]])
        y_test = np.asarray([y.label for y in instances[indices_test]])

        # Fit model.
        self.clf.fit(X_train, y_train)

        # Predict using model.
        y_predict = self.clf.predict(X_test)
        
        # Any exact matches between our whitelist and the instance's word.
        y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances[indices_test]]

        # results are those that are either whitelisted or predicted by the classfier.
        results = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]

        # Accuracy measures.
        accuracy = accuracy_score(y_test, results)
        precision = precision_score(y_test, results)
        recall = recall_score(y_test, results)
        f1 = 2*precision*recall/(precision+recall)

        if self.debug:
            print('\n\nDebugging:')		
            # Print false positives.
            for i in range(len(results)):
                if results[i] != y_test[i] and y_test[i] == 0:
                    print("predicted: {}, actual: {}, instance: {}".format(results[i], y_test[i], instances[indices_test][i]))

            # Print false negatives.
            for i in range(len(results)):
                if results[i] != y_test[i] and y_test[i] != 0:
                    print("predicted: {}, actual: {}, instance: {}".format(results[i], y_test[i], instances[indices_test][i]))

        print('classifier accuracy: %f, precision: %f, recall: %f, f1: %f' % (accuracy, precision, recall, f1))
        
        return accuracy, precision, recall, f1
