import pandas as pd
from mendeleev import element
import itertools
import run
import numpy as np
import sys
import os
from multiprocessing import cpu_count, Pool
from functools import partial
import ast
import pickle
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from itertools import combinations
import matplotlib.pyplot as plt
from scipy.stats import kde

lreg = pd.DataFrame()
basket = pd.DataFrame()
with open (r'./negative_ESI_result.pkl','rb') as f:
    data=pickle.load(f)



# for i in data:
#     tmp = data[i][data[i]['Class'] == 'O2']
#     tmp['dbe'] = tmp['dbe'].astype(int)
#     tmp['C'] = tmp['C'].astype(int)
#     tmp['I'] = tmp['I'].astype(float)
#     acyclic = tmp[tmp['dbe']==1]['I'].sum()
#     cyclic = tmp[(tmp['dbe']>=4)&(tmp['dbe']<=6)]['I'].sum()
#     cyclic2 = tmp[(tmp['dbe']>=7)&(tmp['dbe']<=20)]['I'].sum()
#     basket.loc[i, 'O_ratio'] = acyclic/cyclic
#     basket.loc[i, 'O_ratio2'] = cyclic/cyclic2
#