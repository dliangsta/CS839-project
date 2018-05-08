import pickle
import sys
from collections import defaultdict

metadata = []
def populate_productdict(brand, product_dict):
	f = open('./data/' + brand + '_products.csv', 'r')
	products = f.readlines()
	if len(metadata) == 0:
		metadata.extend(products[0].strip().split(','))
	for i in products[1:]:
		info = i.strip().split(',')
		product_info = {}
		for i in range(1, len(info)):
			product_info[metadata[i]] = info[i]
		product_dict[info[0]] = product_info
		if len(info) != len(metadata):
			print info, len(info)
			assert False
	f.close()


amazon_products = {}
populate_productdict('amazon', amazon_products)

walmart_products = {}
populate_productdict('walmart', walmart_products)

f = open('./data/predicted_matches.csv', 'r')
matches = f.readlines()[1:]
matches = [(i.split(',')[1], i.split(',')[2]) for i in matches]
f.close()

to_print = 'a_id,w_id'
for i in range(1, len(metadata)):	
	meta = metadata[i]
	if meta == 'price':
		to_print += ',amazon_price,walmart_price'
	else:
		to_print += ',' + meta
print to_print

for match in matches:
	if match[0] in amazon_products and match[1] in  walmart_products:
		to_print = match[0] + ',' + match[1]
		#print amazon_products[match[0]], walmart_products[match[1]]
		for i in range(1, len(metadata)):
			meta = metadata[i]
			if meta == 'price':
				to_print += ',' + amazon_products[match[0]][meta]
				to_print += ',' +  walmart_products[match[1]][meta]
			else:
				if amazon_products[match[0]][meta] != '':
					to_print += ',' + amazon_products[match[0]][meta]
				else:
					to_print += ',' + walmart_products[match[1]][meta]
		print to_print