import pickle
from instance import *
from location import *

def main():
    instances = []
    for i in range(1,331):
        with open('data/labeled/' + str(i)) as f:
            data = [line.strip() for line in f.readlines()]
            for i, labeled_line in enumerate(data):
                original_line = data[i-1]
                if i % 2 == 1:
                    labeled_line_split = labeled_line.split(' ')
                    original_line_split = original_line.split(' ')
                    for j, label in enumerate(labeled_line_split):
                        if label[0] == '1':
                            print(label, original_line_split[j])
                            # Make features
                            location = Location(i, j)
                            instance = Instance(location, 1)
                            instances.append(instance)

    with open('data/instances.pkl','wb') as f:
        pickle.dump(instances, f)


if __name__ == '__main__':
    main()