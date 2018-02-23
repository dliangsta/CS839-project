import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score, recall_score, accuracy_score
from instance import *
from location import *
import numpy as np

SPLITS = 5

def main():
    with open('data/I_instances.pkl','rb') as f:
        instances = pickle.load(f)

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

    for k, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, X_test = X[train_index], X[test_index]		
        y_train, y_test = y[train_index], y[test_index]
		
        dt_acc, dt_p, dt_r = decision_tree(X_train, X_test, y_train, y_test)		
        rf_acc, rf_p, rf_r = random_forest(X_train, X_test, y_train, y_test)		
        svm_acc, svm_p, svm_r = svm(X_train, X_test, y_train, y_test)		
        lir_acc, lir_p, lir_r = linear_regression(X_train, X_test, y_train, y_test)		
        lor_acc, lor_p, lor_r = logistic_regression(X_train, X_test, y_train, y_test)
		
        print('fold %d' % k)		
        print('decision tree accuracy: %f, precision: %f, recall: %f' % (dt_acc, dt_p, dt_r))		
        print('random forest accuracy: %f, precision: %f, recall: %f' % (rf_acc, rf_p, rf_r))		
        print('svm accuracy: %f, precision: %f, recall: %f' % (svm_acc, svm_p, svm_r))
        print('linear regression accuracy: %f, precision: %f, recall: %f' % (lir_acc, lir_p, lir_r))
        print('logistic regression accuracy: %f, precision: %f, recall: %f' % (lor_acc, lor_p, lor_r))
		
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
	
    print('Final Results')	
    print('decision tree accuracy: %f, precision: %f, recall: %f' % (dt_acc_cv, dt_p_cv, dt_r_cv))     
    print('random forest accuracy: %f, precision: %f, recall: %f' % (rf_acc_cv, rf_p_cv, rf_r_cv))     
    print('svm accuracy: %f, precision: %f, recall: %f' % (svm_acc_cv, svm_p_cv, svm_r_cv))        
    print('linear regression accuracy: %f, precision: %f, recall: %f' % (lir_acc_cv, lir_p_cv, lir_r_cv))
    print('logistic regression accuracy: %f, precision: %f, recall: %f' % (lor_acc_cv, lor_p_cv, lor_r_cv))
    
    clfs = ['Decision Tree', 'Random Forest', 'SVM', 'Linear Regression', 'Logistic Regression']
    accs = [dt_acc_cv, rf_acc_cv, svm_acc_cv, lir_acc_cv, lor_acc_cv]
    print('\nBest Classifier: ' + clfs[np.argmax(accs)])


def decision_tree(X_train, X_test, y_train, y_test):
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    return accuracy, precision, recall


def random_forest(X_train, X_test, y_train, y_test):
    clf = RandomForestClassifier(random_state=0)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    return accuracy, precision, recall

def svm(X_train, X_test, y_train, y_test):
    clf = SVC()
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    return accuracy, precision, recall

def linear_regression(X_train, X_test, y_train, y_test):
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_predict = np.around(lr.predict(X_test))
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    return accuracy, precision, recall

def logistic_regression(X_train, X_test, y_train, y_test):
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_predict = np.around(lr.predict(X_test))
    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict)
    recall = recall_score(y_test, y_predict)
    return accuracy, precision, recall
        
if __name__ == '__main__':
    main()
    