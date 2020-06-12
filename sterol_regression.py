import main
import pandas as pd
import json
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from itertools import combinations
import concurrent.futures

# take the ratios of two m/z values as input
def simple_linear_regression(packed_arg):
    data, mass, outputtxt = packed_arg
    x, y = mass
    tmp = data[[x, y, 'ccat']].copy()
    tmp = tmp.dropna(how='any', axis=0)
    tmp['new'] = tmp[x]/(tmp[x]+tmp[y])
    tmp = tmp.dropna(how='any', axis=0)
    X_train, X_test, y_train, y_test = train_test_split(tmp['new'], tmp['ccat'], test_size=0.3, random_state=0)
    LR = linear_model.LinearRegression()
    LR.fit(np.array(X_train).reshape(-1, 1), y_train)
    score = LR.score(np.array(X_test).reshape(-1, 1), y_test)
    print(x,y,score)
    if score >= 0.3:
        with open(outputtxt, 'a') as f:
            f.writelines(f'{x, y}, {LR.coef_}, {LR.intercept_}, {score} \n')

test_txt = r'./TestData/Y050053.txt'

## Testing with a small group of laser points
# targeting.raw_txt_filter(raw_txt,'Y053')
# targeting.normalizer(test_csv)

data = main.align(test_txt)
## Add ccat values to each laser point
data=data.set_index('m/z')
data = data.T
## Reduce complexity using dropna
data = data.dropna(axis =1, thresh=0.5*data.shape[0])
colinear = pd.read_csv('./SharedStorage/colinear.csv')
colinear = colinear[colinear['score']>=0.85]
colinear_list = colinear['y'].tolist()
for mass in tuple(colinear_list):
    try:
        data = data.drop(columns=mass)
    except KeyError:
        continue
mass_lists_combinations =list(combinations(data.columns,2))
data = data.T
for column in data.columns:
    data[column] = data[column]/data[column].sum()
data = data.T

with open ('Dict/ccat_avg_dict.json') as f:
    ccat_dict = json.load(f)
data['ccat'] = data.index.map(ccat_dict)
data = data.dropna(subset=['ccat'])
data = data.replace(np.nan,0)
## Use linear regression to predict ccat, with multiprocessing built in
## Breaks the mass_lists
# mass_lists_sliced = {}
# length = len(mass_lists)
# n = 2
# step = int(length / n) + 1
# for mass_start in range(0, length, step):
#     mass_lists_sliced[mass_start] = mass_lists[mass_start:(mass_start + step)]

# mass_lists_combinations = list(zip(mass_lists_sliced[0],mass_lists_sliced[693]))+list(combinations(mass_lists_sliced[0],2))

X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['ccat']), data['ccat'], test_size=0.3, random_state=0)
lr = linear_model.Lasso(alpha=0.1)
lr.fit(X_train, y_train)

args = ((data,mass,'./SharedStorage/shared.txt') for mass in mass_lists_combinations)
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(simple_linear_regression, args)


