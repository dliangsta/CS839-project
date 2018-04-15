spaced_keys = ['32 bit', '32-bit', '64 bit', '64-bit',
               'ac wifi', 'aluminum', 'and', 'anodized', 'anti', 'audio',
               'backlit',  'black', 'blue', 'bluetooth', 'body', 'build', 'burner', 'business', 'buy', 'by',
               'card', 'certified', 'chassis', 'color', 'computer', 'cpu', 'cuk', 'dark',
               'design', 'discontinued', 'disk', 'display', 'drive', 'dvd', 'dvdrw', 'edition', 'eluktronics',
               'english',
               'fingerprint', 'finish', 'flagship', 'flash', 'folio',
               'game', 'gamer', 'gaming', 'generation', 'glare', 'gold', 'graphics', 'gray', 'grey',
               'hard', 'high', 'home',
               'image', 'in', 'inch', 'inch', 'included', 'international',
               'jet',
               'keyboard',
               'laptop', 'led', 'light', 'liight',
               'manufacturer', 'matte', 'maxx', 'memory', 'metal', 'michaelelectronics2', 'mobile', 'model', 'natural',
               'newest', 'notebook', 'new',
               'old', 'operating', 'os',
               'pcaudio', 'pcie', 'performance', 'personal', 'play', 'portable', 'premium', 'pro', 'processor', 'professional', 'profile',
               'ram', 'reader', 'reader', 'red', 'refurbished', 'resistant',
               'screen', 'signature', 'silk', 'silver', 'smart', 'storage', 'style', 'subscription', 'system', 'theoretical',
               'thin', 'to', 'tooth', 'traditional', 'turbo', 'type',
               'ultra', 'ultrabook', 'unknown', 'up',
               'version',
               'warranty', 'water', 'webcam', 'white', 'wi-fi', 'wifi', 'wireless', 'with', 'wlan', 'workstation', 'writer',
               'year']

spaced_keys = [' ' + key + ' ' for key in spaced_keys]
no_space_keys = ['(', ')', '|', '+', '/', '*', '\'', '"', ';', ':', '-', '?']
keys = no_space_keys + sorted(spaced_keys)
for key in keys:
    if len(key) < 4 and len(key) > 1:
        key = ' ' + key.strip() + ' '
    key = key.lower()
    count = 0
    for filename in ['data/labeled.csv', 'data/amazon_products.csv', 'data/walmart_products.csv']:
        out_line = ''
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if key in line:
                    count += 1
                if line != lines[0]:
                    line = line.lower().replace(key, ' ').replace(', ', ',').replace(
                        '  ', ' ').replace('  ', ' ').replace('  ', ' ')
                while line[0] == ' ':
                    line = line[1:]
                out_line += line
        with open(filename, 'w') as f:
            f.write(out_line)
    print(key + ' '*(max([len(key)
                          for key in keys]) + 3 - len(key)) + str(count))
