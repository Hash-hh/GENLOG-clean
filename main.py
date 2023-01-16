from genlog.compare import compare_run
from genlog.csv_split import split_csv
from genlog.csv2xes import csv2xes
from genlog.extract import extract_run
from genlog.resample import resample_run
from genlog.lstm import lstm_run
from genlog.evaluate import evaluate_run
from genlog.measures import measure_run
from genlog.models import model_run

# log_csv_file_name = 'Salt Cavern_resample_test'  # don't add .csv
log_csv_file_name = 'Salt Cavern multimodel'  # don't add .csv


metrics = ['netvol', 'rundensi', 'absunc', 'asunc', 'bsunc',
           'bsunc', 'acurrent', 'bcurrent', 'abdisch',
           'abminf', 'abtotdisch', 'abmanifold', 'abpumpdis']  # salt cavern metrics

# metrics = ['AxisXaaLoad', 'AxisYaaLoad']  # GV12 metrics

model_list = [
    'LSTM',
    # 'prophet',
    # 'ARIMA'
]

measure_list = ['euclidean', 'r2', 'MAE', 'EVS', 'CBD', 'MAPE', 'pearsonr', 'spearmanr',
                                'kendalltau',
                'dtw_distance'
                ]

resample_rate = '1H'
# resample_rate = '100L'

# split_csv(log_csv_file_name, n_splits=3, split_ratio=0.2, monthly=False, yearly=True)
# csv2xes(log_csv_file_name)
extract_run(log_csv_file_name, metrics)
extract_run(log_csv_file_name, metrics, extracted=True)
resample_run(log_csv_file_name, resample_rate=resample_rate)
resample_run(log_csv_file_name, resample_rate=resample_rate, extracted=True)
model_run(log_csv_file_name, model_list)
###### evaluate_run(log_csv_file_name)  # measures used in the original GENLOG paper
compare_run(log_csv_file_name, model_list)
measure_run(log_csv_file_name, measure_list, model_list)  # revised measures