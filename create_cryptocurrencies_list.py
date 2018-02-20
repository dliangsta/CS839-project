import json

def main():
    with open('data/cryptocurrencies_html.html') as f:
        lines = [line.strip() for line in f.readlines()]
        cryptocurrencies = []
        for line in lines:
            # print(line)
            crptocurrency_name = find_cryptocurrency_name(line)
            if crptocurrency_name:
                print(crptocurrency_name)
                cryptocurrencies.append(crptocurrency_name)
    with open('data/cryptocurrencies_list.json','w') as f:
        json.dump(cryptocurrencies, f)

def find_cryptocurrency_name(line):
    # Checked that all cryptos follow title="
    start_index = line.find('title="')
    if start_index >= 0:
        start_index += len('title="')
        # print(line)
        end_index = -1
        for i in range(start_index+1,len(line)):
            if line[i] == '"':
                end_index = i
                return line[start_index:end_index]

if __name__ == '__main__':
    main()