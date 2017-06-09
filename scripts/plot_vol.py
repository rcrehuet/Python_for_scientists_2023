import numpy as np
#import mdtraj as md
import glob
import os.path
import matplotlib.pyplot as plt
#import seaborn.apionly as sns
import seaborn as sns
import pandas as pd
from collections import OrderedDict
#import itertools
plt.ion()

labels = {'p0':0.1, 'p1':1, 'p2':500, 'p3':1000, 'p4':1500, 'p5':2000, 'p6':2500, 
          'p7':3000, 'p8':10}
labels_str={i:str(labels[i]) for i in labels}

Vols =[]
for i in (0,1,8,2,3,4,5,6,7):
    key = "p{}".format(i)
    filenames = glob.glob(os.path.join(key, 'pdbs/*area'))
    filenames.sort()
    for name in filenames:
        msa = {}
        msa['pol'] = 0.0
        msa['np'] = 0.0
        #this was previously done with pd.read_csv but it is slower and does not give
        # any coding advantage
        filein = open(name)
        next(filein)
        for line in filein:
            line = line.split()
            ses = float(line[1])
            atom_name = line[-1]
            atom_name = atom_name[0] #First letter = atomic symbol 
            if atom_name in ('O', 'N'):
                parent = 'pol'
                msa['pol'] += ses
            elif atom_name in ('C', 'S'):
                parent = 'np'
                msa['np'] += ses
            elif atom_name in ('H',):
                msa[parent] += ses
            else: #This should never occur
                print("Problem with line: ", line)
        filein.close()
        Vols.append({'V_hyd':0.38*msa['np'] + 0.03*msa['pol'], 'pressure':key})
       
Vols = pd.DataFrame.from_records(Vols)



Vols2 = pd.DataFrame()
for i in (0,1,8,2,3,4,5,6,7):
    key = "p{}".format(i)
    filename = glob.glob(os.path.join(key, 'pdbs/OutputDir*txt'))[0]
    df = pd.read_csv(filename, sep='\s+',skiprows=7, names =['Protein','V_SE', 
    'Void','VDW', 'Packing_Density',  'Time_Taken'])
    df.drop('Time_Taken', axis=1, inplace=True)
    df.drop('Protein', axis=1, inplace=True)
    #df['pressure'] = key
    df.index = np.arange(Vols[Vols.pressure==key].index[0], 
                         Vols[Vols.pressure==key].index[0]+df.index.size)

    Vols2 = pd.concat([Vols2, df])
 
Vols = pd.concat([Vols, Vols2], axis=1)
Vols.pressure = Vols.pressure.apply(lambda x: labels[x])

Vols['V_tot'] = Vols.Void+Vols.V_hyd

plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.V_hyd, data=Vols, palette='Blues_d')
plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.V_SE, data=Vols, palette='Blues_d')
plt.savefig('images/V_SE.png',dpi=300)
plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.Void, data=Vols, palette='Blues_d')
plt.savefig('images/V_Void.png',dpi=300)
plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.VDW, data=Vols, palette='Blues_d')
plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.Packing_Density, data=Vols, palette='Blues_d')
plt.figure()
sns.boxplot(x=Vols.pressure, y = Vols.V_tot, data=Vols, palette='Blues_d')
plt.savefig('images/V_Tot.png',dpi=300)


