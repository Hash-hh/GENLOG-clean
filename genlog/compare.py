import os
import pandas as pd

def compare_run(log_csv_file_name, model_list):

    for model in model_list:

        predict_path = 'data/csvs/' + log_csv_file_name + '/predicted_data/'
        generate_path = 'data/csvs/' + log_csv_file_name + '/generated/' + model + '/'

        compare_path = 'data/csvs/' + log_csv_file_name + '/compared/' + model + '/'
        if not os.path.exists(compare_path):
            os.makedirs(compare_path)

        for pred_dir in os.listdir(predict_path):
            if not os.path.exists(compare_path+pred_dir):
                os.makedirs(compare_path+pred_dir)

            for (pred_csv, gen_csv) in zip(os.listdir(predict_path+pred_dir), os.listdir(generate_path+pred_dir)):
                pred_df = pd.read_csv(f'{predict_path}{pred_dir}/{pred_csv}', header=None, index_col=0)
                gen_df = pd.read_csv(f'{generate_path}{pred_dir}/{gen_csv}', header=None, index_col=0)

                # pred_df.set_index(pred_df.columns[0], inplace=True)
                # gen_df.set_index(gen_df.columns[0], inplace=True)

                combined_df = pd.concat([pred_df, gen_df], axis=1)
                combined_df = combined_df.dropna()



                combined_df.to_csv(f'{compare_path}{pred_dir}/{pred_csv}', header=None)
