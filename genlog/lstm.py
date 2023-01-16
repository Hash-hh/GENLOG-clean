"""The train model in this file is based on the original LSTM file in the GENLOG paper."""

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import save_model
from keras.models import load_model
from keras.callbacks import EarlyStopping
import pandas as pd
from matplotlib import pyplot as plt
import tensorflow as tf
import os
from matplotlib.lines import Line2D
from numpy import array


def split_series(series, steps):
    """Split the input series into X and y lists for training.

    The X list will contain sublists of length 'steps', and the y list
    will contain the element that follows each sublist in the original
    series.

    For example, if the input series is [1, 2, 3, 4, 5] and the number of
    steps is 2, the X list will be [[1, 2], [2, 3], [3, 4]] and the y list
    will be [3, 4, 5].

    Args:
        series: A list of values to split into X and y lists.
        steps: The number of elements in each sublist of the X list.

    Returns:
        A tuple containing the X list and y list.
    """
    X = []
    y = []
    for i in range(len(series)):
        offset = i + steps
        if offset < len(series)-1:
            X.append(series[i:offset])
            y.append(series[offset])
    return array(X), array(y)

def reshape_X(raw_seq, n_steps):
    """Reshape the X list in the specified list.

    Args:
        raw_seq: A list containing only numbers (no indexing)
        n_steps: Number of elements in each slice

    Returns:
        The reshaped X list.
    """
    # # Load the CSV file into a Pandas DataFrame and extract the second column (index 1) as a NumPy array
    # df = pd.read_csv(csv_file, header=None)
    # raw_seq = df[1].to_numpy()
    # Set the number of steps and split the data into X and y lists
    X, y = split_series(raw_seq, n_steps)
    # Set the number of features and reshape the X list
    n_features = 1
    return X.reshape((X.shape[0], X.shape[1], n_features))



def train_model(resampled_path, generated_path, predicted_path, figures_path, train_csv):
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    train_csv_file = f'{resampled_path}/{train_csv}'  # training on the resampled file

    all_predict_csvs = os.listdir(f'{predicted_path}/{train_csv.split("_")[0]}')  # predict on these csvs


    y_label = train_csv.split('.')[0]
    df = pd.read_csv(train_csv_file, header=None)
    raw_seq = df[1].to_numpy()
    n_steps = 3  # 3
    X, y = split_series(raw_seq, n_steps)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    custom_lines = [Line2D([0], [0], color='red', lw=4), Line2D([0], [0], color='blue', lw=4), Line2D([0], [0], color='purple', lw=4)]
    plt.rcParams.update({'font.size': 24})
    fig, ax = plt.subplots(figsize=(30, 9))
    plt.title('Generated data for ' + train_csv.split('.')[0])
    ax.legend(custom_lines, ['real data', 'generated data', 'prediction data'])
    ax.set(xlabel='time (100ms)', ylabel=y_label)
    num_of_models = len(all_predict_csvs)
    for i in range(num_of_models):
        print("predicting on " + all_predict_csvs[i])
        model = Sequential()
        model.add(LSTM(15, activation='relu', input_shape=(n_steps, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        callbacks = [EarlyStopping(monitor='loss', patience=5)]
        model.fit(X, y, epochs=12, verbose=2, callbacks=callbacks)  # epochs=12

        pred_df = pd.read_csv(f'{predicted_path}/{train_csv.split("_")[0]}/{all_predict_csvs[i]}', header=None)
        pred_date_time = pred_df[0][n_steps:-1]  # skips the first n_steps as they are used to predict the n_steps+1st entry
        pred_raw = pred_df[1].to_numpy()

        X_input = reshape_X(pred_raw, n_steps)

        yhat = model.predict(X_input, verbose=0)

        outpath = f'{generated_path}/{train_csv.split("_")[0]}'
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        pd.DataFrame(yhat, index=pred_date_time).to_csv(f'{outpath}/{all_predict_csvs[i]}',
                                  header=False)  # dump files in the generated folder

        #   ax.plot(range(len(yhat)), yhat, color='blue', linewidth=4)
        ax.scatter(range(len(yhat)), yhat, color='blue')

        ax.scatter(range(len(pred_raw)), pred_raw, color='purple')

        #   ax.plot(range(len(y)), y, color='red', linewidth=3, label='original data')
        ax.scatter(range(len(y)), y, color='red', label='original data')

        fig.savefig(f'{figures_path}/{train_csv.split("_")[0]}.png')


def lstm_run(log_csv_file_name):
    print("lstm training...")

    resampled_path = 'data/csvs/' + log_csv_file_name + '/resampled/'
    generated_path = 'data/csvs/' + log_csv_file_name + '/generated/' + 'LSTM/'
    predicted_path = 'data/csvs/' + log_csv_file_name + '/predicted_data/'
    figures_path = 'data/csvs/' + log_csv_file_name + '/figures/' + 'LSTM/'

    if not os.path.exists(generated_path):
        os.makedirs(generated_path)
    if not os.path.exists(figures_path):
        os.makedirs(figures_path)

    for train_csv in os.listdir(resampled_path):
        print("training on ", train_csv)
        train_model(resampled_path, generated_path, predicted_path, figures_path, train_csv)
    print('\n')




















