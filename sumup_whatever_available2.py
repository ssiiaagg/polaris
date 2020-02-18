import os
import pandas as pd
import numpy as np

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
f = open(r'/Users/siaga/line_test.txt','r')
=======
f = open(r'/Users/siaga/gdgt_test.txt','r')
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
=======
f = open(r'/Users/siaga/gdgt_test.txt','r')
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
=======
f = open(r'/Users/siaga/gdgt_test.txt','r')
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
lines =f.readlines()
samples = {}
basket = pd.DataFrame()
for line in lines:
    data = line.split(';')
    sample_name = data[0]
    samples[sample_name] = pd.DataFrame()
    del data[0]
    del data[0]
    data = pd.DataFrame(np.array(data).reshape((-1,3)),columns=['m/z',sample_name,'S/N'])
    data = data.drop(columns='S/N')
    data = data.astype(float)
    data['m/z'] = data['m/z'].round(2)
    data = data.groupby('m/z').agg({sample_name:sum})
    samples[sample_name] = data.copy()
for sample in samples:
    basket = basket.merge(samples[sample], how ='outer', left_index=True, right_index=True)
basket = basket.reset_index()


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# duplicate_flag = 1
# while duplicate_flag == 1:
#     mass_index = 0
#     duplicate_flag = 0
#     while mass_index < (len(basket)-1):
#         if (basket.loc[mass_index+1,'m/z'] - basket.loc[mass_index,'m/z']) <= 0.01 and (basket.loc[mass_index+1,'m/z'] - basket.loc[mass_index,'m/z']) !=0 :
#             duplicate_flag = 1
#             basket.loc[mass_index,'m/z'] = basket.loc[mass_index+1,'m/z']
#         mass_index = mass_index + 1
# basket = basket.groupby('m/z').sum()
basket.to_pickle("./gdgt_similarMassMerged_Y50.pkl")
=======
=======
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
=======
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
duplicate_flag = 1
while duplicate_flag == 1:
    mass_index = 0
    duplicate_flag = 0
    while mass_index < (len(basket)-1):
        if (basket.loc[mass_index+1,'m/z'] - basket.loc[mass_index,'m/z']) <= 0.01 and (basket.loc[mass_index+1,'m/z'] - basket.loc[mass_index,'m/z']) !=0 :
            duplicate_flag = 1
            basket.loc[mass_index,'m/z'] = basket.loc[mass_index+1,'m/z']
        mass_index = mass_index + 1
basket = basket.groupby('m/z').sum()
basket.to_pickle("./gdgt_similarMassMerged.pkl")
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
=======
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
=======
>>>>>>> 2cfc163034ecf24df37ccc7cad1f3fb1ed7182fb
