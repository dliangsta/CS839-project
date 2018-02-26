import pickle
from classify import Classifier

class Extractor:
    def __init__(self, clf):
        self.clf = clf

    def extract(self, docs):
        for doc in docs:
            for i, line in enumerate(doc):
                # Consider strings with 1 or 2 words in them, typical for cryptocurrencies.
                words = line.split(' ')
                for j in [1, 2]:
                    for k in range(len(words)-1):
                        # TODO: Vectorize, then run CV.
                        print(' '.join(words[k:k+j]))

def main():
    with open('data/I_docs.pkl','rb') as f:
        docs = pickle.load(f)
    extractor = Extractor(Classifier('dt'))
    extractor.extract(docs)


if __name__ == '__main__':
    main()

    