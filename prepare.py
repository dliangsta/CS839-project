import json
import sys

def main():

    directory = 'data/'
    names = ['aishwarya','david','vish']
    for name in names:
        
        with open(directory + name + '_raw.json') as f:
            data = json.load(f) 


        out = ''
        for article in data:
            # Clean article.
            article = article.replace('  ',' ').replace(' \n','\n').replace('\n ','\n').replace('\n\n','\n')
            # Split into lines.
            lines = article.split('\n')

            for line in lines:
                line = line.strip() + '.'
                if len(line) > 0:
                    out += line + '\n'
                    words = line.split(' ')

                    for i in range(len(words)):
                        out_line = '`' + '_' * (len(words[i])-1) + ' '
                        out += out_line

                    out += '\n'

            out += '\n'

        print(out)    
        with open(directory + name + '_prepared.txt','w') as f:
            f.write(out)
        

def write(out):
    sys.stdout.write(out)
    sys.stdout.flush()

if __name__ == '__main__':
    main()

