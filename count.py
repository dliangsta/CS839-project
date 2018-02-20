# Counts stuff

def main():
    # Number of mentions of cryptocurrency. We want 800+.
    one_count = 0
    # Number of mentions of bitcoin.
    bitcoin_count = 0
    # Number of documents with no mentions of a cryptocurrency.
    none_count = 0
    for i in range(1,331):
        with open('data/labeled/' + str(i)) as f:
            pre_one_count = one_count
            
            data = [line.strip() for line in f.readlines()]
            for i, line in enumerate(data):
                if i % 2 == 1:
                    one_count += line.count('1')
                if i % 2 == 0:
                    bitcoin_count += line.lower().count('bitcoin')

            if one_count == pre_one_count:
                none_count += 1

    print(one_count, bitcoin_count, none_count)

if __name__ == '__main__':
    main()