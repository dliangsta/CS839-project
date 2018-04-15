import json

def main():
    # Number of mentions of cryptocurrency. We want 800+.
    one_count = 0
    # Number of mentions of bitcoin.
    bitcoin_count = 0
    # Number of documents with no mentions of a cryptocurrency.
    none_count = 0
    nones = []
    for i in range(1,331):
        try:
            with open('data/labeled/' + str(i)) as f:
                pre_one_count = one_count
                
                data = [line.strip() for line in f.readlines()]
                for j, line in enumerate(data):
                    if j % 2 == 1:
                        one_count += line.count('1')
                    elif j % 2 == 0:
                        bitcoin_count += line.lower().count('bitcoin')

                if one_count == pre_one_count:
                    none_count += 1
                    nones.append(i)
        except:
            pass

    print(one_count, bitcoin_count, none_count)
    print(nones)

    with open('data/no_mentions.json', 'w') as f:
        json.dump(nones, f)

if __name__ == '__main__':
    main()