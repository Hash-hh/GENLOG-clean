"""This file gets the correlation metrix of a log (csv) file."""

import seaborn as sns
import pandas as pd
import os

log_csv_file_name = 'Salt Cavern'
csv_path = '../data/csvs/' + log_csv_file_name + '/csv_splits/'
results_path = '../data/csvs/' + log_csv_file_name + '/results/'
if not os.path.exists(results_path):
    os.makedirs(results_path)

for csv in os.listdir(csv_path):

    metrics = ['netvol', 'rundensi', 'absunc', 'asunc', 'bsunc',
               'bsunc', 'acurrent', 'bcurrent', 'abdisch',
               'abminf', 'abtotdisch', 'abmanifold', 'abpumpdis']

    df = pd.read_csv('../data/csvs/' + log_csv_file_name + '/csv_splits/'+csv).iloc[:, 1:14].T
    df.index = metrics
    df.drop(columns=df.columns[0], axis=1, inplace=True)

    corr_map = sns.clustermap(df.T.corr(), annot=True,
                   fmt='.2f',
                   cmap=sns.diverging_palette(h_neg=20,
                                              h_pos=220), center=0)
    fig = corr_map.fig
    fig.savefig(f'{results_path}corr{csv.split("-")[0]}.pdf')

