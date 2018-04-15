import pickle
import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score, recall_score, accuracy_score
from instance import *
from location import *

SPLITS = 5

def main():
    with open('data/I_instances.pkl','rb') as f:
        instances = np.asarray(pickle.load(f))
    with open('data/cryptocurrencies_list.json') as f:
        cryptocurrencies = json.load(f)
    with open('data/cryptocurrency_abbreviations_list.json') as f:
        cryptocurrency_abbreviations = json.load(f)
    whitelist = [word.lower() for word in cryptocurrencies[:25] + cryptocurrency_abbreviations[:25]]


    X = np.asarray([x.features for x in instances])
    y = np.asarray([x.label for x in instances])

    kf = KFold(n_splits=SPLITS)
    kf.get_n_splits(X)

    dt_acc_cv = 0
    rf_acc_cv = 0
    svm_acc_cv = 0
    lir_acc_cv = 0
    lor_acc_cv = 0

    dt_p_cv = 0
    rf_p_cv = 0
    svm_p_cv = 0
    lir_p_cv = 0
    lor_p_cv = 0

    dt_r_cv = 0
    rf_r_cv = 0
    svm_r_cv = 0
    lir_r_cv = 0
    lor_r_cv = 0

    dt_f1_cv = 0
    rf_f1_cv = 0
    svm_f1_cv = 0
    lir_f1_cv = 0
    lor_f1_cv = 0


    for k, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, X_test = X[train_index], X[test_index]		
        y_train, y_test = y[train_index], y[test_index]
        instances_test = instances[test_index]
		
        dt_acc, dt_p, dt_r, dt_f1 = decision_tree(X_train, X_test, y_train, y_test, instances_test, whitelist)		
        rf_acc, rf_p, rf_r, rf_f1 = random_forest(X_train, X_test, y_train, y_test, instances_test, whitelist)		
        svm_acc, svm_p, svm_r, svm_f1 = svm(X_train, X_test, y_train, y_test, instances_test, whitelist)		
        lir_acc, lir_p, lir_r, lir_f1 = linear_regression(X_train, X_test, y_train, y_test, instances_test, whitelist)		
        lor_acc, lor_p, lor_r, lor_f1 = logistic_regression(X_train, X_test, y_train, y_test, instances_test, whitelist)
		
        print('fold %d' % k)		
        print('decision tree accuracy: %f, precision: %f, recall: %f, f1: %f' % (dt_acc, dt_p, dt_r, dt_f1))		
        print('random forest accuracy: %f, precision: %f, recall: %f, f1: %f' % (rf_acc, rf_p, rf_r, rf_f1))		
        print('svm accuracy: %f, precision: %f, recall: %f, f1: %f' % (svm_acc, svm_p, svm_r, svm_f1))
        print('linear regression accuracy: %f, precision: %f, recall: %f, f1: %f' % (lir_acc, lir_p, lir_r, lir_f1))
        print('logistic regression accuracy: %f, precision: %f, recall: %f, f1: %f' % (lor_acc, lor_p, lor_r, lor_f1))
		
        dt_acc_cv += dt_acc		
        rf_acc_cv += rf_acc		
        svm_acc_cv += svm_acc		
        lir_acc_cv += lir_acc		
        lor_acc_cv += lor_acc

        dt_p_cv += dt_p
        rf_p_cv += rf_p
        svm_p_cv += svm_p
        lir_p_cv += lir_p
        lor_p_cv += lor_p

        dt_r_cv += dt_r
        rf_r_cv += rf_r
        svm_r_cv += svm_r
        lir_r_cv += lir_r
        lor_r_cv += lor_r

        dt_f1_cv += dt_f1
        rf_f1_cv += rf_f1
        svm_f1_cv += svm_f1
        lir_f1_cv += lir_f1
        lor_f1_cv += lor_f1
	
    dt_acc_cv /= SPLITS	
    rf_acc_cv /= SPLITS	
    svm_acc_cv /= SPLITS	
    lir_acc_cv /= SPLITS	
    lor_acc_cv /= SPLITS

    dt_p_cv /= SPLITS
    rf_p_cv /= SPLITS
    svm_p_cv /= SPLITS
    lir_p_cv /= SPLITS
    lor_p_cv /= SPLITS

    dt_r_cv /= SPLITS
    rf_r_cv /= SPLITS
    svm_r_cv /= SPLITS
    lir_r_cv /= SPLITS
    lor_r_cv /= SPLITS

    dt_f1_cv /= SPLITS
    rf_f1_cv /= SPLITS
    svm_f1_cv /= SPLITS
    lir_f1_cv /= SPLITS
    lor_f1_cv /= SPLITS
	
    print('\n\nFinal Results')	
    print('decision tree accuracy: %f, precision: %f, recall: %f, f1: %f' % (dt_acc_cv, dt_p_cv, dt_r_cv, dt_f1_cv))     
    print('random forest accuracy: %f, precision: %f, recall: %f, f1: %f' % (rf_acc_cv, rf_p_cv, rf_r_cv, rf_f1_cv))     
    print('svm accuracy: %f, precision: %f, recall: %f, f1: %f' % (svm_acc_cv, svm_p_cv, svm_r_cv, svm_f1_cv))        
    print('linear regression accuracy: %f, precision: %f, recall: %f, f1: %f' % (lir_acc_cv, lir_p_cv, lir_r_cv, lir_f1_cv))
    print('logistic regression accuracy: %f, precision: %f, recall: %f, f1: %f' % (lor_acc_cv, lor_p_cv, lor_r_cv, lor_f1_cv))
    
    clfs = ['Decision Tree', 'Random Forest', 'SVM', 'Linear Regression', 'Logistic Regression']
    accs = [dt_acc_cv, rf_acc_cv, svm_acc_cv, lir_acc_cv, lor_acc_cv]
    print('\nBest Classifier: ' + clfs[np.argmax(accs)])


def decision_tree(X_train, X_test, y_train, y_test, instances_test, whitelist):
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances_test]
    predicted = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]
    accuracy = accuracy_score(y_test, predicted)
    precision = precision_score(y_test, predicted)
    recall = recall_score(y_test, predicted)
    f1 = 2*precision*recall/(precision+recall)
    return accuracy, precision, recall, f1


def random_forest(X_train, X_test, y_train, y_test, instances_test, whitelist):
    clf = RandomForestClassifier(random_state=0)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances_test]
    predicted = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]
    accuracy = accuracy_score(y_test, predicted)
    precision = precision_score(y_test, predicted)
    recall = recall_score(y_test, predicted)
    f1 = 2*precision*recall/(precision+recall)
    return accuracy, precision, recall, f1

def svm(X_train, X_test, y_train, y_test, instances_test, whitelist):
    clf = SVC()
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances_test]
    predicted = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]
    accuracy = accuracy_score(y_test, predicted)
    precision = precision_score(y_test, predicted)
    recall = recall_score(y_test, predicted)
    f1 = 2*precision*recall/(precision+recall)
    return accuracy, precision, recall, f1

def linear_regression(X_train, X_test, y_train, y_test, instances_test, whitelist):
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_predict = np.around(lr.predict(X_test))
    y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances_test]
    predicted = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]
    accuracy = accuracy_score(y_test, predicted)
    precision = precision_score(y_test, predicted)
    recall = recall_score(y_test, predicted)
    f1 = 2*precision*recall/(precision+recall)
    return accuracy, precision, recall, f1

def logistic_regression(X_train, X_test, y_train, y_test, instances_test, whitelist):
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_predict = np.around(lr.predict(X_test))
    y_whitelist = [int(any([white == instance.stripped_lowered_word for white in whitelist])) for instance in instances_test]
    predicted = [1 if y >= 1 else 0 for y in y_predict + y_whitelist]
    accuracy = accuracy_score(y_test, predicted)
    precision = precision_score(y_test, predicted)
    recall = recall_score(y_test, predicted)
    f1 = 2*precision*recall/(precision+recall)
    return accuracy, precision, recall, f1
        
if __name__ == '__main__':
    main()
    