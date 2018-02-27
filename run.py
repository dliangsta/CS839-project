import json
import pickle
from sklearn.model_selection import KFold
from classify import *
import argparse

class CryptoCurrencyExtractor:
    def __init__(self, clf):
        self.clf = clf

    def train_and_classify(self, dev_set_instances, test_set_instances):
        results = self.clf.classify(instances=dev_set_instances, 
                                       test_instances = test_set_instances)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rules_on', action='store_true', help='whether to apply post processing rules after classification')
    parser.add_argument('--debug_on', action='store_true', help='Debug on?')
    args = parser.parse_args()
    with open('data/I_instances.pkl','rb') as f:
        dev_set_instances = np.asarray(pickle.load(f))
    with open('data/J_instances.pkl','rb') as f:
        test_set_instances = np.asarray(pickle.load(f))
    crypto_extractor = CryptoCurrencyExtractor(Classifier('rf', rules_on = args.rules_on, debug = args.debug_on))
    crypto_extractor.train_and_classify(dev_set_instances, test_set_instances)

if __name__ == '__main__':
    main()
    