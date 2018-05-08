import pandas as pd
import mlxtend
from collections import defaultdict
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import sys
df = pd.read_csv('./data/merged_clean_numeric_v2.csv')

suffixes = {}
suffixes['hard disk size'] = ' GB'
suffixes['processor speed'] = ' GHz'
suffixes['screen size'] = ' in'
suffixes['ram size'] = ' GB'

#'processor (cpu) manufacturer'
all_dict = defaultdict(list)
for data in df:
	if data in ['brand', 'hard disk size', 'operating system', 'processor count', 'processor speed', 'ram size', 'screen size']:
		for i in range(0, len(df[data])):
			all_dict['id'].append(i)
			val = str(data).replace(' ', '_') + ': ' + str(df[data][i])
			if data in suffixes:
				val = val + suffixes[data]
			all_dict['value'].append(val)
			all_dict['qty'].append(1)

df = pd.DataFrame(data=all_dict)
basket = (df
          .groupby(['id', 'value'])['qty']
          .sum().unstack().reset_index().fillna(0)
          .set_index('id'))

frequent_itemsets = apriori(basket, min_support=0.45, use_colnames=True)

'''
print ('Support\tLengthofSet\tFrequent_Item_Set')
for i in range(0, len(frequent_itemsets['support'])):
	support = frequent_itemsets['support'][i]
	itemsets = frequent_itemsets['itemsets'][i]
	to_print = ''
	for item in itemsets:
		to_print += ', ' + item

	to_print = str(round(support, 2)) + '\t' + str(len(itemsets)) + '\t[' + to_print[1:] + ' ]'
	print (to_print)
sys.exit(0)
'''

rules = association_rules(frequent_itemsets)
rules = rules[(rules['confidence'] >= 0.8)]

print ('AssociationRule\tSupport\tConfidence')
for i in range(0, len(rules['support'])):
	print (str(rules['antecedants'][i]).replace('frozenset', '') + ' => ' + str(rules['consequents'][i]).replace('frozenset', '') + '\t' + str(round(rules['support'][i],2)) + '\t' + str(round(rules['confidence'][i],2)))