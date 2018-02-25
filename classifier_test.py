import pickle
import json
import numpy as np
from classifier import *

def main():
    with open('data/I_instances.pkl','rb') as f:
        instances = np.asarray(pickle.load(f))
    with open('data/cryptocurrencies_list.json') as f:
        cryptocurrencies = json.load(f)
    with open('data/cryptocurrency_abbreviations_list.json') as f:
        cryptocurrency_abbreviations = json.load(f)

    clf = Classifier('dt',debug=False)
    whitelist = [word.lower() for word in cryptocurrencies[:25] + cryptocurrency_abbreviations[:25]]
    clf.classify(instances, whitelist)

if __name__ == '__main__':
    main()
    