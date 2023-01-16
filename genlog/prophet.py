import os
import pandas as pd
from neuralprophet import NeuralProphet
import matplotlib.pyplot as plt

def train_model(resampled_path, generated_path, predicted_path, figures_path, train_csv):
    train_csv_file = f'{resampled_path}/{train_csv}'  # training on the resampled file
    all_predict_csvs = os.listdir(f'{predicted_path}/{train_csv.split("_")[0]}')  # predict on these csvs
    df = pd.read_csv(train_csv_file, header=None)
    df.columns = ['ds', 'y']
    num_of_models = len(all_predict_csvs)

    for i in range(num_of_models):

        # instantiate a new NeuralProphet model
        model = NeuralProphet()

        # fit the model to your data
        model.fit(df)

        print("predicting on " + all_predict_csvs[i])

        # Make predictions on the test data
        pred_df = pd.read_csv(f'{predicted_path}/{train_csv.split("_")[0]}/{all_predict_csvs[i]}', header=None)
        pred_df.columns = ['ds', 'y']

        # create a dataframe to hold future predictions
        future_data = model.make_future_dataframe(periods=365, df=df)

        # make predictions
        forecast = model.predict(pred_df)
        # print(forecast.columns)

        # get predicted values
        predicted_values = [value[0] for value in forecast[['yhat1']].values]


        # # pred_raw = pred_df[1].to_numpy()
        # pred_raw = pd.Series(pred_df.iloc[:, 1])
        #
        # print("start: ", pred_raw.index[0])
        #
        # predictions = model.predict(start=pred_raw.index[0], end=pred_raw.index[-1])
        #
        outpath = f'{generated_path}/{train_csv.split("_")[0]}'
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        pd.DataFrame(predicted_values, index=pred_df['ds']).to_csv(f'{outpath}/{all_predict_csvs[i]}',
                                                        header=False)  # dump files in the generated folder

        # Plot the actual values and predictions
        model.plot(forecast)
        # plt.plot(pred_raw, label='Actual values')
        # plt.plot(predictions, label='Predictions')
        plt.legend()
        plt.savefig(f'{figures_path}/{train_csv.split("_")[0]}.png')


def prophet_run(log_csv_file_name):
    print("Auto Regression training...")

    resampled_path = 'data/csvs/' + log_csv_file_name + '/resampled/'
    generated_path = 'data/csvs/' + log_csv_file_name + '/generated/' + 'prophet/'
    predicted_path = 'data/csvs/' + log_csv_file_name + '/predicted_data/'
    figures_path = 'data/csvs/' + log_csv_file_name + '/figures/' + 'prophet/'

    if not os.path.exists(generated_path):
        os.makedirs(generated_path)
    if not os.path.exists(figures_path):
        os.makedirs(figures_path)

    for train_csv in os.listdir(resampled_path):
        print("training on ", train_csv)
        train_model(resampled_path, generated_path, predicted_path, figures_path, train_csv)
    print('\n')
