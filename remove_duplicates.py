import json
import os

def main():
    remove_duplicates()
    shift_document_names_down()


def remove_duplicates():
    with open ('data/duplicate_documents.json') as f:
        data = json.load(f)

    with open('data/no_mentions.json') as f:
        data += json.load(f)

    data = list(set(data))
    print(data)
    print(len(data))
    for i in data:
        os.remove('data/labeled/'+str(i))
        os.remove('data/unlabeled/'+str(i))

def shift_document_names_down():
    i = 1
    passes_with_no_shifts = 0
    while i < 371:
        try:
            open('data/unlabeled/'+str(i))
            print('opened ' + str(i))
            i += 1
        except:
            if not passes_with_no_shifts:
                print('failed to open ' + str(i) + ', shifting documents down')
            shifted = 0
            for j in range(i+1,371):
                try:
                    open('data/unlabeled/' + str(j))
                    os.rename('data/unlabeled/' + str(j), 'data/unlabeled/' + str(j-1))
                    os.rename('data/labeled/' + str(j), 'data/labeled/' + str(j-1))
                    shifted += 1
                except:
                    pass
            if shifted == 0:
                passes_with_no_shifts += 1
            if passes_with_no_shifts == 100:
                exit()

if __name__ == '__main__':
    main()
