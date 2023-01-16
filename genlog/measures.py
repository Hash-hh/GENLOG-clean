import os
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_log_error, explained_variance_score, mean_absolute_percentage_error
from scipy.stats import pearsonr, spearmanr, kendalltau
import bz2
from dtw import dtw
from dtaidistance.dtw import distance as dtw_distance



def euclidean(val1, val2):
    diff = np.array(val1) - np.array(val2)
    l2 = np.linalg.norm(diff, ord=2)
    max_l2 = np.linalg.norm(np.ones(len(val1)), ord=2)
    return l2 / max_l2

def CBD(val1, val2):
    # b1 = bin(int(''.join(map(str, val1)), 2) << 1)
    # b2 = bin(int(''.join(map(str, val2)), 2) << 1)
    c1 = bz2.compress(val1)
    c2 = bz2.compress(val2)
    b12 = val1 + val2
    c12 = bz2.compress(b12)

    return len(c12)/(len(c1)*len(c2))

def measure_run(log_csv_file_name: str, list_of_measures: list, model_list: list):

    for model in model_list:

        compare_path = 'data/csvs/' + log_csv_file_name + '/compared/' + model + '/'
        measures_path = 'data/csvs/' + log_csv_file_name + '/measures/' + model + '/'
        if not os.path.exists(measures_path):
            os.makedirs(measures_path)

        measure_funcs = {'euclidean': euclidean, 'r2': r2_score, 'MAE': mean_absolute_error,
                         'EVS': explained_variance_score, 'MAPE': mean_absolute_percentage_error,
                         'pearsonr': pearsonr, 'spearmanr': spearmanr, 'kendalltau': kendalltau,
                         'CBD': CBD, 'dtw_distance': dtw_distance
                         }
        measures_df = pd.DataFrame(columns=([m for m in list_of_measures]))


        for metric in os.listdir(compare_path):  # loop over all metrics in compared directory

            for comp_csv in os.listdir(compare_path+metric):  # loop over all csv files in a metric folder

                df = pd.read_csv(f'{compare_path}/{metric}/{comp_csv}', header=None)
                val1 = df.iloc[:,1].to_numpy()
                val2 = df.iloc[:,2].to_numpy()

                for measure in list_of_measures:  # loop over all measures
                    measures_df.at[comp_csv.split('.')[0], measure]= measure_funcs[measure](val1, val2)

        measures_df.to_csv(measures_path+f'measures_{model}.csv')



