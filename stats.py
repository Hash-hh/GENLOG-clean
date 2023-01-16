"""This files is used to get summary statistics of a log (csv) file"""

import pandas as pd

metrics = ['netvol', 'rundensi', 'absunc', 'asunc', 'bsunc',
           'bsunc', 'acurrent', 'bcurrent', 'abdisch',
           'abminf', 'abtotdisch', 'abmanifold', 'abpumpdis']


# df = pd.read_csv('data/logs/Salt Cavern.csv', header=None, usecols=range(1,14))
df = pd.read_csv('data/logs/GVdata.csv')
# df.columns = metrics

desc = df.describe().drop(['25%','50%','75%']).transpose()
desc.to_csv('data/logs/GV desc.csv')
desc.to_latex('data/logs/GV desc.txt')
# desc.to_latex('data/logs/Salt Cavern desc.txt')


