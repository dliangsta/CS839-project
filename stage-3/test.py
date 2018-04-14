import sys
import py_entitymatching as em
import pandas as pd
import os

# Get the paths
path_A = 'data/amazon_products.csv'
path_B = 'data/walmart_products.csv'

# Load csv files as dataframes and set the key attribute in the dataframe
A = em.read_csv_metadata(path_A, key='id')
B = em.read_csv_metadata(path_B, key='id')

brands = ['gigabyte','lg', 'alienware', 'microsoft', 'huawei', 'rca', 'razer', 'iview', 'toshiba',
          'hp', 'dell', 'lenovo', 'prostar', 'acer', 'samsung', 'apple', 'asus', 'panasonic', 'msi']
models = ['satellite','alpha','vivo','leopard','transformer','precision','460','470','560','570','p50','p51','p70','p71','aero','sabre','miix','titan','gram','gl','aw', 'aspire', 'swift', 'spin', 'strix', 'raider', 'cambio', 'nitro', 'matebook', 'viking', 'probook', 'phantom', 'helios', 'triton', 'stream', 'blade', 'zenbook', 'zephyrus', 'flex', 'notebook', 'colorwheel', 'surface', 'chromebook',
          'vivobook', 'maximus', 'zenbook', 'flex', 'ativ', 'apache', 'predator', 'x360', 'stealth', 'omen', 'xps', 'carbon', 'x1', 'yoga', 'envy', 'thinkpad', 'latitude', 'inspiron', 'elitebook', 'clevo', 'spectre', 'macbook', 'pavilion', 'ideapad', 'legion']
# sizes = ['12','13','14','15','16','17']

def match_make_model(a, b):
    # if for all value sets, there is a value that is in both tuples, return false (keep tuple).
    # otherwise return true (drop tuple).
    a_combo = a['combo']
    b_combo = b['combo']
    valuesets = [brands, models]
    i = 0
    n = len(valuesets)
    while i < n:
        valueset = valuesets[i]
        j = 0
        m = len(valueset)
        match = False
        while j < m:
            value = valueset[j]
            if value in a_combo and value in b_combo:
                # end loop
                j = m
                # mark as match
                match = True
            j += 1
        if not match:
            # drop tuple
            return True
        i += 1
    return False

# 30x slower oneliner:
#     return not all(
#         [any([value in a['combo'] and value in b['combo']] for value in valueset)
#          for valueset in [brands, models, cpus]])


count = 0
for i in range(len(A)):
    if match_make_model(A.iloc[i], A.iloc[i]):
        print(A.iloc[i]['combo'])
        print()
        count += 1
for i in range(len(B)):
    if match_make_model(B.iloc[i], B.iloc[i]):
        print(B.iloc[i]['combo'])
        print()
        count += 1


print(count)