import sys
import argparse



def extract_matches():
	with open('./data/Table_E.csv', 'r') as f:
		lines = f.readlines()

	header = lines[0].strip().split(',')
	a_index = header.index('#a_id')
	w_index = header.index('w_id')

	with open('./data/matches.txt', 'w') as f:
		f.write('a_id\t\tw_id\n')
		for row in lines[1:]:
			values = row.strip().split(',')
			a_id = values[a_index]
			w_id = values[w_index]

			f.write('%s\t\t%s\n' % (a_id, w_id))



def main():
	extract_matches()

if __name__ == '__main__':
	main()