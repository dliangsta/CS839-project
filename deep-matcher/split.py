# split labeled into train test val
import sys
import py_entitymatching as em
import pandas as pd
import os

path_A = '/home/liang/Workspace/cs839-project/stage-3/data/amazon_products.csv'
path_B = '/home/liang/Workspace/cs839-project/stage-3/data/walmart_products.csv'

# Load the csv files as dataframes and set the key attribute in the dataframe
A = em.read_csv_metadata(path_A, key='id')
B = em.read_csv_metadata(path_B, key='id')
print('len(A):' + str(len(A)))
print('len(B):' + str(len(B)))
print('len (A X B):' + str(len(A)*len(B)))
path_S = 'data/original.csv'
S = em.read_csv_metadata(path_S, 
                         key='id',
                         ltable=A, rtable=B, 
                         fk_ltable='left_id', fk_rtable='right_id')
IJ = em.split_train_test(S, train_proportion=0.6, random_state=0)
I = IJ['train']
J = IJ['test']
JK = em.split_train_test(J, train_proportion=.5, random_state=0)
J = JK['train']
K = JK['test']
I.to_csv('data/train.csv')
J.to_csv('data/validation.csv')
K.to_csv('data/test.csv')
print(I,J,K)