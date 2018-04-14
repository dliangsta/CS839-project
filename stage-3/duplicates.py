for filename in ['data/labeled.csv','data/walmart_products.csv','data/amazon_products.csv']:
    ids = []
    new_f = ''
    count = 0
    with open(filename,'r+') as f:
        lines = f.readlines()
        for line in lines:
            if 'unknown' in line:
                count += 1
            new_f += line.replace('unknown','')
        f.seek(0)
        f.write(new_f)
        f.truncate()

    print(count)