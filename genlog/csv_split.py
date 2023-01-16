import csv
from datetime import datetime
import random
import os


def split_csv(log_csv_file_name, n_splits, split_ratio=1, monthly=False, yearly=False):
    """
    Split a CSV file into n_splits number of randomly sampled files.

    Parameters:
        log_csv_file_name (str): The name of the CSV file in the data/logs folder.
        n_splits (int): The number of random splits of the CSV file.
        split_ratio (float): The percentage of entries to select from the csv folder
        monthly (bool): If True, split the csv file wrt months
        yearly (bool): If True, split the csv file wrt years
    """


    # checking if both monthly and yearly are True
    if monthly & yearly:
        raise "Both monthly and yearly are True."

    print("Splitting CSV file...")

    # Open the input CSV file
    with open(f"data/logs/{log_csv_file_name}.csv", newline='') as fr:
        # Create the output directory if it does not exist
        split_csv_path = f'data/csvs/{log_csv_file_name}/csv_splits'
        if not os.path.exists(split_csv_path):
            os.makedirs(split_csv_path)

        if monthly or yearly:

            # Create a CSV reader object
            reader = csv.reader(fr)

            # Initialize a variable to store the current month
            current_month = None
            current_year = None

            # Initialize a variable to store the current file
            current_file = None

            # A list of format strings to try
            FORMAT_STRINGS = ["%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M"]

            # Iterate over the rows in the CSV
            for row in reader:
                # select this row to be processed based on split_ratio
                if random.uniform(0, 1) > split_ratio:
                    continue

                # Parse the timestamp in the first column
                timestamp = None
                for format_string in FORMAT_STRINGS:
                    try:
                        timestamp = datetime.strptime(row[0], format_string)
                        break
                    except ValueError:
                        continue

                # print(row)

                # If the month/year has changed, close the current file
                # and open a new file for the new month/year
                if monthly:
                    if timestamp.month != current_month:
                        current_month = timestamp.month
                        if current_file is not None:
                            current_file.close()
                        current_file = open(f"{split_csv_path}/{timestamp.year}-{timestamp.month}.csv", "w", newline='')
                        writer = csv.writer(current_file, quoting=csv.QUOTE_MINIMAL)

                if yearly:
                    if timestamp.year != current_year:
                        current_year = timestamp.year
                        if current_file is not None:
                            current_file.close()
                        current_file = open(f"{split_csv_path}/{timestamp.year}.csv", "w", newline='')
                        writer = csv.writer(current_file, quoting=csv.QUOTE_MINIMAL)

                # Write the row to the current file
                writer.writerow(row)

            # Don't forget to close the final file
            if current_file is not None:
                current_file.close()

        else:  # randomly

            # Create the output files
            filenames = [f'{split_csv_path}/split_{i}.csv' for i in range(n_splits)]
            filedata = {filename: open(filename, 'w') for filename in filenames}

            # Read the input CSV file line by line and write each line to a random output file
            for entry in fr:
                if random.uniform(0, 1) > split_ratio:
                    continue

                f = random.choice(filenames)
                filedata[f].write(entry)
