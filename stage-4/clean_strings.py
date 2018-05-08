import pickle
import sys
import argparse

# 'Computer Upgrade King', go to product title and select second element
# 'MichaelElectronics2' or 'EXcaliberPC' or 'Beach Camera', go to product title and select first element
brands = [['Dell', 'Dell USA', 'Dell Computers', 'Dell Consumer', 'Dell Commercial'],
		  ['Acer', 'XOTIC PC'],
		  ['HP', 'HP-14-4GB-32GB', 'hp', 'UpgradePro', 'HP Stream Laptop', 'HP Flagship Laptop', 'Hewlett Packard', 'HP-Stream-14-4GB-32GB', 'HP US'],
		  ['Lenovo', 'Lenovo Group Limited', 'Lenovo Laptops', 'Lenovo-ideapad-320', 'Lenovo USA', 'Laptop Authority', 'Lenovo INC', 'Flex 4'],
		  ['Asus', 'ASUS', 'ASUS Computers', 'HIDevolution'],
		  ['CTL'],
		  ['Prostar'],
		  ['MSI'],
		  ['Apple', 'Apple Computer', 'DigitalAndMore', 'GoodDeal Electronics & Apple'],
		  ['Razer'],
		  ['Samsung'],
		  ['Toshiba'],
		  ['Alienware'],
		  ['LG'],
		  ['Bit'],
		  ['Panasonic', 'Quality Refurbished Computers'],
		  ['Microsoft'],
		  ['SLIDE'],
		  ['VIZIO'],
		  ['Aorus'],
		  ['Huawei']]

lcts = [['Touchscreen', 'Business 2-in-1 Laptop', 'Home and Business Full HD IPS Touchscreen Laptop', 'Home and Business HD Touchscreen Laptop', 'Home and Business Full HD Touchscreen Laptop'],
		['Chromebook', 'Chrome', 'Chrome OS', 'Chromebooks', 'Home and Education Chromebook'],
		['Gaming Laptop', 'Gaming Laptops'],
		['PC', 'Home and Business Full HD IPS Laptop', 'Home and Business Full HD IPS Laptop', 'Home and Education Laptop', 'PC Laptops', 'PC; Notebook', 'Windows 7 Professional 64', 'Windows'],
		['Macbook', 'Mac', 'MacBooks']]

os_s = [['Windows 10', '64-bit Windows 10 Pro', 'Microsoft Windows', 'Microsoft Windows 10', 'Microsoft Windows 10 Pro', 'Win 10', 'Windows 10 Home', 'Windows 10 Home 64', 'Windows 10 Home 64-Bit', 'Windows 10 Home 64-bit', 'Windows 10 Home 64bit English', 'Windows 10 Home 64-bit English', 'Windows 10 Home x64-bit', 'Windows 10 Microsoft Signature Image', 'Windows 10 Pro', 'Windows 10 Pro 64', 'Windows 10 Pro 64-bit Edition', 'Windows 10 Pro 64-bit Edition Academic', 'Windows 10 Professional', 'Windows 10 Professional 64-bit', 'Windows 10 Professional Windows 7 Professional', 'Windows 10 S', 'Windows 10 x64-bit', 'windows 10 professional', 'Unknown', 'other'],
		['Windows 7', 'Windows 7 Pro', 'Windows 7 Professional', 'Windows 7 Professional 64', 'Windows 7 Professional 64 (available through downgrade rights from Windows 10 Pro 64)', 'Windows 7;'],
		['Windows 8', 'Windows 8.1', 'Windows 8;'],
		['Chrome', 'Chrome OS'],
		['Mac OS X', 'Mac OS 9.X', 'Mac OS Sierra', 'Mac OS X 10.12 Sierra', 'Mac OS X 10.2 Jaguar', 'Mac OS X 10.8 Mountain Lion', 'Mac OS X El Capitan', 'Mac OS X Mavericks', 'Mac OS X V10.11 El Capitan', 'Mac OS X v10.8 Mountain Lion', 'OS X Mavericks']]

intel = ['intel', 'Intel', 'Celeron', 'celeron', 'Pentium', 'pentium', 'i5', 'i7', 'Atom', 'Core', '8032', 'None', 'core_m', 'GHz']
samsung = ['Exynos']
rockchip = ['Rockchip']
amd = ['AMD', 'Athlon', 'athlon']

def print_brands(csv):
	seen = {}
	with open('./data/' + csv, 'r') as f:
		lines = f.readlines()

	header = lines[0].strip().split(',')
	brand_index = header.index('brand')

	for row in lines[1:]:
		values = row.strip().split(',')
		brand = values[brand_index]
		if brand not in seen:
			seen[brand] = True
			print(brand)


def clean_csv(dirty_csv):
	with open('./data/' + dirty_csv, 'r') as f:
		lines = f.readlines()

	header = lines[0].strip().split(',')
	title_index = header.index('product title')
	brand_index = header.index('brand')
	#lct_index = header.index('laptop computer type')
	os_index = header.index('operating system')
	cpu_index = header.index('processor (cpu) manufacturer')

	clean = [','.join(header)]
	for row in lines[1:]:
		values = row.strip().split(',')
		
		title = values[title_index]
		brand = values[brand_index]
		#lct = values[lct_index]
		os = values[os_index]
		cpu = values[cpu_index]

		# first clean brand
		print('cleaning brand')
		if brand in ['MichaelElectronics2', 'EXcaliberPC', 'Beach Camera']:
			brand = title.split()[0]
		elif brand == 'Computer Upgrade King':
			brand = title.split()[1]

		for b in brands:
			if brand in b:
				brand = b[0]
				break

		# next clean lct
		#print('cleaning lcts')
		#for l in lcts:
		#	if lct in l:
		#		lct = l[0]
		#		break

		# next clean os
		print('cleaning os')
		for o in os_s:
			if os in o:
				os = o[0]
				break

		# finally clean cpu manufacturer
		print('cleaning cpu')
		for i in intel:
			if i in cpu:
				cpu = 'Intel'
				break
		for i in amd:
			if i in cpu:
				cpu = 'AMD'
				break
		for i in samsung:
			if i in cpu:
				cpu = 'Samsung'
				break
		for i in rockchip:
			if i in cpu:
				cpu = 'Rockchip'
				break

		# now place values back into csv
		values[brand_index] = brand
		#values[lct_index] = lct
		values[os_index] = os
		values[cpu_index] = cpu

		# now write line to clean file
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