import pickle
import sys
import argparse
from collections import defaultdict 
def clean_csv(dirty_csv):
	with open('./data/' + dirty_csv, 'r') as f:
		lines = f.readlines()

	['display resolution', 'laptop computer type', 'average battery life']
	old_header = lines[0].strip().split(',')
	header = []
	for column in old_header:
		if column not in ['display resolution', 'laptop computer type', 'average battery life']:
			header.append(column)
	print ''
	print header
	amazon_price_index = header.index('amazon_price')
	clean = [','.join(header)]

	for row in lines[1:]:
		values = row.strip().split(',')
		#amazon_price = float(values[amazon_price_index].replace('$', '').replace(',', ''))
		#values[amazon_price_index] = str(amazon_price)
		new_values = []
		for i in range(0, len(values)):
			if old_header[i] not in ['display resolution', 'laptop computer type', 'average battery life']:
				new_values.append(values[i])
		# now write line to clean file
		clean.append(','.join(new_values))
	return clean


def write_clean_csv(clean_schema, clean_csv):
	with open('./data/' + clean_csv, 'w') as c:
		for line in clean_schema:
			c.write('%s\n' % line)

def main(args):
	dirty_file = args.dirty
	clean_file = args.clean

	clean_schema = clean_csv(dirty_file)
	write_clean_csv(clean_schema, clean_file)
	#print_brands(dirty_csv)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('--dirty',
						help='dirty csv file',
						type=str,
						required=True)

	parser.add_argument('--clean',
						help='clean csv file',
						type=str,
						required=True)

	args = parser.parse_args()
	main(args)