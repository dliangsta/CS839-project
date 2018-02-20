import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
import numpy as np

def main():
    with open('data/instances.pkl','rb') as f:
        dataset = pickle.load(f)
    print(dataset[0])

def decision_tree(X, y):
    clf = DecisionTreeClassifier(random_state=0)

def random_forest(X, y):
    clf = RandomForestClassifier(max_depth=2, random_state=0)

def svm(X, y):
    clf = SVC()

def linear_regression(X, y):
    lr = LinearRegression()

def logistic_regression(X, y):
    lr = LogisticRegression()
        
if __name__ == '__main__':
    main()
    