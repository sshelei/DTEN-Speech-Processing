import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
import numpy as np
import sys

def dict_to_csv (data, csv_file):
    if not data:
        raise ValueError("The input dictionary is empty.")

    # Extract headers from the first entry (metrics keys)
    first_key = next(iter(data))
    headers = ["filename"] + list(data[first_key].keys())

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for filename, metrics in data.items():
            row = {"filename": filename, **metrics}
            writer.writerow(row)

def evaluate_audio_files(dirname, metrics, save_csv_file):
    results = {}
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if not file.endswith(".wav"):
                continue
            results[file] = {}
            for metric in metrics:
                results[file][metric] = get_metric(audio) # temp placeholder function, replace with actual calls to get metric
    dict_to_csv(results, save_csv_file)

def load_csv (csv_file):
    try:
        data = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    return data


def plot_metric (csv_file, metric, save_path, filename, bins_=20, figsize_=(9,5)):
    # process the csv file
    csv_data = load_csv(csv_file)
    if csv_data is None:
        return
    
    # extract data
    try:
        data = csv_data[metric]
    except KeyError:
        print(f"Error extracting column {metric} from '{csv_file}'")
        return
    
    # set bins
    data_min = data.min()
    data_max = data.max()
    bins = np.linspace(data_min, data_max, bins_)
  
    # graph
    plt.figure(figsize=figsize_)
    plt.hist(data, bins=bins, log=True, alpha=0.3, align='mid', edgecolor='black')
  
    # round x-axis
    x_ticks = plt.xticks()[0]
    rounded_x_ticks = np.round(x_ticks, decimals=2)
    plt.xticks(x_ticks, rounded_x_ticks)
    plt.xlim(data_min, data_max)

    # label axis and title
    plt.xlabel(metric)
    plt.ylabel("Count")
    csv_name = os.path.basename(csv_file)
    plt.title(f"{metric}_distribution_for_{csv_name}")
    plt.grid(True, alpha=0.3)
    
    # save
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(os.path.join(save_path, filename))

def plot_metric_comparison (clean_csv, restored_csv, metric, save_path, filename, bins_=20, figsize_=(9,5)):
    # process csv files 
    clean_data = load_csv(clean_csv)
    restored_data = load_csv(restored_csv)
    if ((clean_data is None) or (restored_data is None)):
        return

    # extract data
    try:
        clean_col = clean_data[metric]
    except KeyError:
        print(f"Error extracting column {metric} from '{clean_csv}'")
        return
    try:
        restored_col = restored_data[metric]
    except KeyError:
        print(f"Error extracting column {metric} from '{restored_csv}'")
        return

    # extract labels
    clean_label = os.path.basename(clean_csv)
    restored_label = os.path.basename(restored_csv)

    # set bins
    data_min = min(clean_col.min(), restored_col.min())
    data_max = max(clean_col.max(), restored_col.max())
    bins = np.linspace(data_min, data_max, bins_)

    # graphs (filled bars + outlines)
    plt.figure(figsize=figsize_)
    plt.hist(clean_col, bins=bins, log=True, alpha=0.3, align='mid', label=clean_label, color='red', edgecolor="black")
    plt.hist(restored_col, bins=bins, log=True, alpha=0.3, align='mid', label=restored_label, color='blue', edgecolor="black")
    plt.hist(clean_col, bins=bins, histtype="step", linewidth=1.8, color="red")
    plt.hist(restored_col, bins=bins, histtype="step", linewidth=1.8, color="blue")

    # round x axis
    x_ticks = plt.xticks()[0]
    rounded_x_ticks = np.round(x_ticks, decimals=2)
    plt.xticks(x_ticks, rounded_x_ticks)
    plt.xlim(data_min, data_max)

    # label axis and title
    plt.xlabel(metric)
    plt.ylabel("Count")
    plt.title(f"{metric}_distribution_for_{clean_label}_vs_{restored_label}.png")
    plt.legend()  
    plt.grid(True, alpha=0.3)

    # save
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(os.path.join(save_path, filename))
  

if __name__ == "__main__":
    # set parameters here
    csv_file_1 = "/root/data/ears_v2_normal.csv"
    csv_file_2 = "/root/data/ears_v2.csv"
    metric = "SOK"
    filename = "test.png"
    save_path = "/root/data/"

    # function calls
    plot_metric_comparison(csv_file_1, csv_file_2, metric, save_path, "comparison.png")
    plot_metric(csv_file_1, metric,  save_path, filename)