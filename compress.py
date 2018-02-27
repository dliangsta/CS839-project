# Compress each document into one line.

for i in range(1,301):
    with open('data/labeled/'+str(i),'r+') as f:
        text = ''
        labels = ''
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                text += line
            else:
                labels += line
        text = text.replace('\n', ' ').replace('  ', ' ')
        labels = labels.replace('\n', ' ').replace('  ', ' ')
        print(text)
        print(labels)
        print(text + '\n' + labels)
        f.seek(0)
        f.write(text + '\n' + labels)
        f.truncate()
        