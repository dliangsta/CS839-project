import sys
import argparse
import numpy as np
from random import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, accuracy_score

labels = ['$0-$200', '$200-$400', '$400-$600', '$600-$800', '$800-$1000', '$1000-$1200',
		   '$1200-$1400', '$1400-$1600', '$1600-$1800', '$1800-$2000', '$2000-$2200',
		   '$2200-$2400', '$2400-$2600', '$2600-$2800', '$2800-$3000', '$3000-$3200',
		   '$3200-$3400', '$3400-$3600', '$3600-$3800', '$3800-$4000', '$4000-$4200',
		   '$4200-$4400', '$4400-$4600', '$4600-$4800', '$4800-$5000', '$5000-$5200',
		   '$5200-$5400', '$5400-$5600', '$5600-$5800', '$5800-$6000', '$6000-$6200',
		   '$6200-$6400', '$6400-$6600']

def create_data(in_csv):
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
	shuffle(data)

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

	X = np.array(X)
	y = np.array(y)
	
	# now encode strings as categorical features
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
	#X = np.concatenate((X, os_s), axis=1)

	X = X.astype(np.float64)
	y = y.astype(np.float64)

	# categorize prices into $200 quantile buckets
	num_buckets = (6600 / 200) + 1

	buckets = list(range(0, 6800, 200))
	indices = np.digitize(y, bins=buckets, right=True)
	y_cat = np.empty(y.shape, dtype=object)

	# replace all values with categorical label strings
	for i in range(len(y)):
		for j in range(len(y[i])):
			y_cat[i,j] = labels[indices[i,j]-1]


	#print(y_cat[:10])

	return  X, y_cat


def predict_prices(X, y):

	# convert string labels to numerical
	le = LabelEncoder()
	le.fit(labels)
	y_a = le.transform(y[:,0])
	y_w = le.transform(y[:,1])
	y = np.stack((y_a, y_w), axis=1)

	dt = DecisionTreeClassifier(random_state=0)
	rf = RandomForestClassifier(random_state=0)
	#nb = GaussianNB()
	#lr = LogisticRegression()

	models = [(dt, 'Decision Tree'),
			  (rf, 'Random Forest')]#,
			  #(lr, 'Logistic Regression')]#,
			  #(nb, 'Gaussian Naive Bayes')]

	# split X,y into train and test
	split_index = int(np.ceil((2.0/3) * len(X)))
	
	X_train = X[:split_index]
	X_test = X[split_index:]

	y_train = y[:split_index]
	y_test = y[split_index:]

	# Train models and make predictions using the testing set
	for model in models:
		clf = model[0]
		clf.fit(X_train, y_train)
		y_pred = clf.predict(X_test)

		# Statistics
		a_accuracy = accuracy_score(y_test[:,0], y_pred[:,0])
		a_precision = precision_score(y_test[:,0], y_pred[:,0], average='weighted')
		a_recall = recall_score(y_test[:,0], y_pred[:,0], average='weighted')
		try:
			a_f1 = 2*a_precision*a_recall/(a_precision+a_recall)
		except:
			a_f1 = -1.

		w_accuracy = accuracy_score(y_test[:,1], y_pred[:,1])
		w_precision = precision_score(y_test[:,1], y_pred[:,1], average='weighted')
		w_recall = recall_score(y_test[:,1], y_pred[:,1], average='weighted')
		try:
			w_f1 = 2*w_precision*w_recall/(w_precision+w_recall)
		except:
			w_f1 = -1.

		# print results
		print('\nClassifier: %s' % model[1])
		print('Accuracy:\tamazon - %.3f\twalmart - %.3f' % (a_accuracy, w_accuracy))
		print('Precision:\tamazon - %.3f\twalmart - %.3f' % (a_precision, w_precision))
		print('Recall:\tamazon - %.3f\twalmart - %.3f' % (a_recall, w_recall))
		print('F1:\tamazon - %.3f\twalmart - %.3f' % (a_f1, w_f1))

	# view predictions
	#pred_vs_real = np.concatenate((y_test, y_pred), axis=1)
	#print(pred_vs_real[:20])

	return None


def main(args):
	input_file = args.input

	X, y = create_data(input_file)
	predictions = predict_prices(X, y)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('--input',
						help='input csv file',
						type=str,
						required=True)
	
	args = parser.parse_args()
	main(args)