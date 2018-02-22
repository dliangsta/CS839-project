import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from instance import *
from location import *
import numpy as np

SPLITS = 10

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

    for k, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, X_test = X[train_index], X[test_index]		
        y_train, y_test = y[train_index], y[test_index]
		
        dt_acc = decision_tree(X_train, X_test, y_train, y_test)		
        rf_acc = random_forest(X_train, X_test, y_train, y_test)		
        svm_acc = svm(X_train, X_test, y_train, y_test)		
        lir_acc = linear_regression(X_train, X_test, y_train, y_test)		
        lor_acc = logistic_regression(X_train, X_test, y_train, y_test)
		
        print('fold %d' % k)		
        print('decision tree accuracy: %f' % dt_acc)		
        print('random forest accuracy: %f' % rf_acc)		
        print('svm accuracy: %f' % svm_acc)		
        print('linear regression accuracy: %f' % lir_acc)	
        print('logistic regression accuracy: %f\n' % lor_acc)
		
        dt_acc_cv += dt_acc		
        rf_acc_cv += rf_acc		
        svm_acc_cv += svm_acc		
        lir_acc_cv += lir_acc		
        lor_acc_cv += lor_acc
	
    dt_acc_cv /= SPLITS	
    rf_acc_cv /= SPLITS	
    svm_acc_cv /= SPLITS	
    lir_acc_cv /= SPLITS	
    lor_acc_cv /= SPLITS
	
    print('Final Results')	
    print('decision tree accuracy: %f' % dt_acc_cv)	
    print('random forest accuracy: %f' % rf_acc_cv)	
    print('svm accuracy: %f' % svm_acc_cv)	
    print('linear regression accuracy: %f' % lir_acc_cv)	
    print('logistic regression accuracy: %f\n' % lor_acc_cv)
    
    clfs = ['Decision Tree', 'Random Forest', 'SVM', 'Linear Regression', 'Logistic Regression']
    accs = [dt_acc_cv, rf_acc_cv, svm_acc_cv, lir_acc_cv, lor_acc_cv]
    print('\nBest Classifier: ' + clfs[np.argmax(accs)])


def decision_tree(X_train, X_test, y_train, y_test):
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)


def random_forest(X_train, X_test, y_train, y_test):
    clf = RandomForestClassifier(random_state=0)
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)

def svm(X_train, X_test, y_train, y_test):
    clf = SVC()
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)

def linear_regression(X_train, X_test, y_train, y_test):
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    return lr.score(X_test, y_test)

def logistic_regression(X_train, X_test, y_train, y_test):
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    return lr.score(X_test, y_test)
        
if __name__ == '__main__':
    main()
    