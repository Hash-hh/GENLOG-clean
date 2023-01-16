from genlog.lstm import lstm_run
from genlog.ARIMA import ARIMA_run
from genlog.prophet import prophet_run

def model_run(log_csv_file_name, model_list):
    models_dict = {'LSTM': lstm_run, 'ARIMA': ARIMA_run, 'prophet': prophet_run
                     }

    for model in model_list:
        run_func = models_dict[model]
        run_func(log_csv_file_name)