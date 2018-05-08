import pickle
import sys
import argparse
from collections import defaultdict 

def clean_csv(dirty_csv):
	with open('./data/' + dirty_csv, 'r') as f:
		lines = f.readlines()
	header = lines[0].strip().split(',')
	amazon_price_index = header.index('amazon_price')
	walmart_price_index = header.index('walmart_price')
	hard_disk_size_index = header.index('hard disk size')
	processor_count_index = header.index('processor count')
	processor_speed_index = header.index('processor speed')
	ram_size_index = header.index('ram size')

	screen_size_index = header.index('screen size')

	clean = [','.join(header)]

	for row in lines[1:]:
		values = row.strip().split(',')
		
		amazon_price = float(values[amazon_price_index].replace('$', '').replace(',', ''))
		values[amazon_price_index] = str(amazon_price)
		
		walmart_price = (values[walmart_price_index].replace('$', '').replace(',', ''))
		if walmart_price == 'N/A':
			values[walmart_price_index] = ''
		else:
			values[walmart_price_index] = str(float(walmart_price))
			if float(walmart_price) < 100.0:
				values[walmart_price_index] = ''

		hard_disk_size = values[hard_disk_size_index]
		hard_disk_size_val = 0
		if hard_disk_size != '':
			hard_disk_size_val = float(hard_disk_size.split(' ')[0])
			if len(hard_disk_size.split(' ')) == 2:
				assert hard_disk_size.split(' ')[1] in ['Terabytes', 'TB' ,'GB', 'KB']
				if hard_disk_size.split(' ')[1] in ['Terabytes', 'TB']:
					hard_disk_size_val = hard_disk_size_val * 1000.0

		hard_disk_size = str(hard_disk_size_val)
		if hard_disk_size_val < 1.0:	
			hard_disk_size = ''
		values[hard_disk_size_index] = hard_disk_size

		processor_speed = values[processor_speed_index]
		processor_speed_val = 0
		if processor_speed != '':
			processor_speed_val = float(processor_speed.split(' ')[0])
			if len(processor_speed.split(' ')) >= 2:
				assert processor_speed.split(' ')[1] in ['GHz', 'Gigahertz' , 'Hz', 'MHz']
				if processor_speed.split(' ')[1] == 'MHz':
					processor_speed_val = (processor_speed_val/1000.0)

		processor_speed = str(processor_speed_val)
		if processor_speed_val < 0.1 or processor_speed_val > 5.0:
			processor_speed = ''
		values[processor_speed_index] = processor_speed

		ram_size = values[ram_size_index]
		assert len(ram_size.split(' ')) == 2 and ram_size.split(' ')[-1] == 'GB'
		ram_size_val = float(ram_size.split(' ')[0])
		ram_size = str(ram_size_val)
		if ram_size_val <= 0.2:
			ram_size = ''
		values[ram_size_index] = ram_size


		screen_size_val = float(values[screen_size_index].replace('in', ''))
		screen_size = str(screen_size_val)
		if screen_size_val < 5.0:
			screen_size = ''
		values[screen_size_index] = screen_size

		# remove missing rows
		missing = False
		for value in values:
			if value == '':
				missing = True
				break
		if not missing:
			clean.append(','.join(values))
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