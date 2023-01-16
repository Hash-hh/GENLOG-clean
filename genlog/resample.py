import os
import pandas as pd


def resample(inpath, outpath, resample_rate):

    for infile in os.listdir(inpath):
        df = pd.read_csv(inpath + infile)
        # TODO: Also add the option to average the duplicates
        df = df.drop_duplicates(subset=['timestamp'])
        df.index = df.timestamp
        df = df.drop('timestamp', axis=1)
        df.index = pd.to_datetime(df.index)
        df = df.resample(resample_rate).pad()
        # df = df.resample(resample_rate).interpolate()
        ### df = df.resample('100L').pad()  # resample with 100 ms (100L)
        df = df.dropna()
        df = df.reset_index()
        # df = df.drop('timestamp', axis=1)
        df.set_index('timestamp')
        write_csv(df, outpath, infile)

def write_csv(df, path2, file):
    df.to_csv(path2 + file, header=False, index=False)


def resample_run(log_csv_file_name: str, extracted: bool = False, resample_rate: str = '1H') -> None:
    """
    Resample the data in the input path and write the results to the output path.

    Parameters:
    - log_csv_file_name: the name of the log CSV file
    - extracted: a boolean indicating whether the input data has been extracted
                 from the log CSV file (default: False)

    Returns: None
    """
    print("Resampling...")

    # Determine the base path for the input and output files
    if extracted:
        inbasepath = 'data/csvs/' + log_csv_file_name + '/extracted/'
        base_output_path = 'data/csvs/' + log_csv_file_name + '/predicted_data/'
        for extracted_folder in os.listdir(inbasepath):
            inpath = inbasepath + '/' + extracted_folder + '/'
            outpath = base_output_path + '/' + extracted_folder + '/'
            # Create the out path if one does not exist
            if not os.path.exists(outpath):
                os.makedirs(outpath)

            resample(inpath, outpath, resample_rate)
    else:
        inpath = 'data/csvs/' + log_csv_file_name + '/single_runs/'
        outpath = 'data/csvs/' + log_csv_file_name + '/resampled/'

        if not os.path.exists(outpath):
            os.makedirs(outpath)

        resample(inpath, outpath, resample_rate)





