# Counts the number of mentions of cryptocurrency. We want 800+.

def main():
    one_count = 0
    bitcoin_count = 0
    for i in range(1,331):
        with open('data/labeled/' + str(i)) as f:
            data = [line.strip() for line in f.readlines()]
            for i, line in enumerate(data):
                if i % 2 == 1:
                    one_count += line.count('1')
                if i % 2 == 0:
                    bitcoin_count += line.lower().count('bitcoin')
    print(one_count)
    print(bitcoin_count)

if __name__ == '__main__':
    main()