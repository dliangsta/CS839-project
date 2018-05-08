import sys
import argparse
import numpy as np
from random import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def predict_prices(in_csv):
	with open('./data/' + in_csv, 'r') as f:
		lines = f.readlines()

	header = lines[0].strip().split(',')
	
	# gather csv indices of each attribute
	aprice_idx = header.index('amazon_price')
	wprice_idx = header.index('walmart_price')
	brand_idx = header.index('brand')
	hds_idx = header.index('hard disk size')
	os_idx = header.index('operating system')
	cpum_idx = header.index('processor (cpu) manufacturer')
	pcount_idx = header.index('processor count')
	pspeed_idx = header.index('processor speed')
	ram_idx = header.index('ram size')
	screen_idx = header.index('screen size')

	data = lines[1:]
	#shuffle(data)

	# X will represent our feature vectors, y will be the prices
	X = []
	y = []

	brands = []
	os_s = []
	cpums = []

	# parse data and create feature vectors
	for row in data:
		values = row.strip().split(',')

		aprice = values[aprice_idx]
		wprice = values[wprice_idx]
		brand = values[brand_idx]
		hds = values[hds_idx]
		os = values[os_idx]
		cpum = values[cpum_idx]
		pcount = values[pcount_idx]
		pspeed = values[pspeed_idx]
		ram = values[ram_idx]
		screen = values[screen_idx]

		features = np.array([hds, pcount, pspeed, ram, screen])
		X.append(features)
		prices = np.array([aprice, wprice])
		y.append(prices)

		brands.append(brand)
		os_s.append(os)
		cpums.append(cpum)

	# now encode strings as categorical features
	X = np.array(X)
	y = np.array(y)

	label_encoder = LabelEncoder()
	onehot_encoder = OneHotEncoder(sparse=False)

	# brand
	integer_encoded = label_encoder.fit_transform(brands) # transform strings to integers
	integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
	onehot_encoded = onehot_encoder.fit_transform(integer_encoded) # transform integers to one-hot encoding
	brands = onehot_encoded

	# os
	integer_encoded = label_encoder.fit_transform(os_s) # transform strings to integers
	integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
	onehot_encoded = onehot_encoder.fit_transform(integer_encoded) # transform integers to one-hot encoding
	os_s = onehot_encoded

	# cpu manufacturer
	integer_encoded = label_encoder.fit_transform(cpums) # transform strings to integers
	integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
	onehot_encoded = onehot_encoder.fit_transform(integer_encoded) # transform integers to one-hot encoding
	cpums = onehot_encoded

	X = np.concatenate((X, brands, os_s, cpums), axis=1)

	print(X[:10])
	return  None



def write_csv(predictions, out_csv):
	with open('./data/' + out_csv, 'w') as c:
		for line in clean_schema:
			c.write('%s\n' % line)


def main(args):
	input_file = args.input
	output_file = args.output

	predictions = predict_prices(input_file)
	#write_csv(predictions, output_file)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('--input',
						help='input csv file',
						type=str,
						required=True)

	parser.add_argument('--output',
						help='output csv file',
						type=str,
						required=True)

	args = parser.parse_args()
	main(args)