import main
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import itertools
import concurrent.futures
from sklearn import linear_model
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def cut_ccat(dataframe,n):
    ccat_list = dataframe['ccat'].tolist()
    ccat_tuple = sorted(tuple(ccat_list))
    ccat_label_list = []
    step = int(len(ccat_tuple) / n) + 1
    for i in range(0, len(ccat_tuple) + 1, step):
        ccat_label_list.append(ccat_tuple[i])
    ccat_label_list.append(ccat_tuple[-1])
    return ccat_label_list


def ccat_label(ccat, ccat_label_list):
    for i in range(0,len(ccat_label_list)-1):
        if (ccat >= ccat_label_list[i]) & (ccat < ccat_label_list[i+1]):
            return i



def colinear_finder(packed_arg):
    data, mass = packed_arg
    x, y = mass
    tmp = data[[x, y]].copy()
    tmp = tmp.dropna(how='any', axis=0)
    X_train, X_test, y_train, y_test = train_test_split(np.array(tmp[x]).reshape(-1,1), tmp[y], test_size=0.2, random_state=0)
    LR = linear_model.LinearRegression()
    LR.fit(np.array(X_train).reshape(-1, 1), y_train)
    score = LR.score(np.array(X_test).reshape(-1, 1), y_test)
    print(x,y,score)
    with open('./SharedStorage/colinear.txt', 'a') as f:
        f.writelines(f'{x, y,score} \n')


# classify laser points with high and low ccat values
# test_txt = r'./TestData/Y050053.txt'
test_txt = r'/Users/siaga/Documents/gdgt/sbb_sterol.txt'
raw_data = main.align(test_txt)
raw_data = raw_data.set_index('m/z')
# for column in raw_data.columns:
#     raw_data[column] = (raw_data[column] - raw_data[column].min()) / (raw_data[column].max() - raw_data[column].min())
raw_data = raw_data.T
raw_data = raw_data.dropna(axis =1, thresh=0.8*raw_data.shape[0])
raw_data = raw_data.dropna(thresh=0.5*raw_data.shape[1])
raw_data = raw_data.dropna(subset=[433.38])

# mass_lists_combinations =list(itertools.combinations(raw_data.columns,2))
#
# args = ((raw_data,mass) for mass in mass_lists_combinations)
#
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     executor.map(colinear_finder, args)

##exclude colinear m/z
colinear = pd.read_csv('./SharedStorage/colinear.csv')
colinear = colinear[colinear['score']>=0.7]
colinear_list = colinear['y'].tolist()
for mass in tuple(colinear_list):
    try:
        raw_data = raw_data.drop(columns=mass)
    except KeyError:
        continue

raw_data = raw_data.T
for column in raw_data.columns:
    raw_data[column] = raw_data[column]/raw_data[column].sum()
raw_data = raw_data.T
##add ccat info
with open ('Dict/ccat_avg_dict.json') as f:
    ccat_dict = json.load(f)
raw_data['ccat'] = raw_data.index.map(ccat_dict)
raw_data = raw_data.dropna(subset=['ccat'])

raw_data['label'] = raw_data['ccat'].round(2)
raw_data = raw_data.drop(columns=['ccat'])

raw_data = raw_data[raw_data['label'].isin([0.44,0.51])]
raw_data['label'] = raw_data['label'].astype(str)
## cut ccat ranges
# cuts = 4
# ccat_label_list = cut_ccat(raw_data,cuts)
#
#
# ## classify the points to ccat_labels
# raw_data['label'] = raw_data['ccat'].apply(ccat_label,args=(ccat_label_list,))

raw_data  = raw_data.replace(np.nan, 0)
X_train, X_test, y_train, y_test = train_test_split(raw_data.drop(columns='label'), raw_data['label'], test_size=0.2,random_state=0)
clf = LinearDiscriminantAnalysis()
# clf = QuadraticDiscriminantAnalysis()
clf.fit(X_train,y_train)
xda = clf.fit_transform(X_train,y_train)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xda[:,0], xda[:,1], xda[:,2], s=50,c=y_train,cmap='rainbow', alpha=0.7,edgecolors='black')
plt.show()

# # scalings of each variable
# scalings = pd.DataFrame(clf.scalings_,columns = [f'LD{i}' for i in range(0,cuts-1)] )
# scalings.index = raw_data.drop(columns='label').T.index



# plt.xlabel('LD1')
# plt.ylabel('LD2')
# plt.scatter(
# xda[:,0],
# xda[:,1],
# c=y_train,
# cmap='rainbow',
# alpha=0.7,
# edgecolors='b'
# )
