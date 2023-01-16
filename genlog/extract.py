import pm4py
import yaml
import os
import json
import csv

def Sort(li):
    first = li.pop(0)
    li = sorted(li, key = lambda x: x[1])
    li.insert(0,first)
    return li

def write_csv(file, output):
    with open(file, 'w+', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(output)

def extract_xes(log_csv_file_name, metric, split_xes_file, save_path):
    # Construct the path to the split XES file
    split_xes_file_path = f'data/csvs/{log_csv_file_name}/xes_splits/{split_xes_file}'

    # Read the event log from the split XES file
    event_log = pm4py.read_xes(split_xes_file_path)

    # Extract the metric data from the event log
    metric_data = [['value','timestamp']]
    for trace in event_log:
        for event in trace:
            if metric in event:
                timestamp = event['time:timestamp']
                metric_data.append([event[metric], timestamp])

    # Sort the metric data by timestamp
    if len(metric_data) > 2:
        metric_data = Sort(metric_data)

    # Write the metric data to a CSV file
    if metric_data:
        postscript = split_xes_file
        if "_" in postscript:
            postscript = postscript.split("_")[-1].split(".")[0]
        write_csv(f"{save_path}/{metric}_{postscript}.csv", metric_data)

def extract_run(log_csv_file_name, metrics, extracted=False):

    print("Extracting...")

    if extracted:

        for metric in metrics:
            # Determine the base path for the output files
            base_path = f'data/csvs/{log_csv_file_name}/extracted/{metric}'

            # Create the base path if it does not exist
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            # Get the list of split XES files
            split_xes_path = f'data/csvs/{log_csv_file_name}/xes_splits'
            split_xes_files = os.listdir(split_xes_path)

            # Determine which files to process based on the extracted flag
            files_to_process = split_xes_files[1:]

            # Extract XES files for each metric
            for split_xes_file in files_to_process:
                extract_xes(log_csv_file_name, metric, split_xes_file, base_path)

    else:

        for metric in metrics:
            # Determine the base path for the output files
            base_path = f'data/csvs/{log_csv_file_name}/single_runs/'

            # Create the base path if it does not exist
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            # Get the list of split XES files
            split_xes_path = f'data/csvs/{log_csv_file_name}/xes_splits'
            split_xes_files = os.listdir(split_xes_path)

            # Determine which files to process based on the extracted flag
            files_to_process = [split_xes_files[0]]

            # Extract XES files for each metric
            for split_xes_file in files_to_process:
                extract_xes(log_csv_file_name, metric, split_xes_file, base_path)
