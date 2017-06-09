import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import OrderedDict

plt.ion()

labels = {'p1':1, 'p2':1000, 'p3':2500}
labels_str={i:str(labels[i]) for i in labels}



df_list = []
for i in (1,2,3):
    key = "p{}".format(i)
    filename = "../notebooks/data/p{}.dat".format(i)
    df = pd.read_csv(filename, sep='\s+',skiprows=7, names =['Protein','V_SE', 
    'Void','VDW', 'Packing_Density',  'Time_Taken'])
    df.drop('Time_Taken', axis=1, inplace=True)
    df.drop('Protein', axis=1, inplace=True)
    df['pressure'] = key
    df_list.append(df)

Vols = pd.concat(df_list, ignore_index=True)
 

Vols.pressure = Vols.pressure.apply(lambda x: labels[x])

plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.Void, data=Vols, palette='Blues_d')
plt.figure()
sns.boxplot(x="pressure", y = "Packing_Density", data=Vols, palette='Blues_d')
plt.figure()
sns.regplot(x="pressure", y="Packing_Density", data=Vols,x_estimator=np.mean)

