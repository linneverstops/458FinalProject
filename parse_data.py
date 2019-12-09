# file that contains functions to parse data
import csv
import numpy as np
import pandas as pd


def parse_data():
    with open('fitbitdata.csv') as f:
        reader = csv.reader(f)
        data = []
        for r in reader:
            del r[0]
            data.append(r)
        legend = data.pop(0)
        data = np.array(data).astype(np.float64)
        return data, legend


def parse_data_panda():
    fitbit_data = pd.read_csv('fitbitdata.csv')
    fitbit_data.info()
    fitbit_data.head()
    fitbit_data['Date'] = pd.to_datetime(fitbit_data['Date'])
    date_plot = fitbit_data.set_index('Date').plot(subplots=True, figsize=(10, 50))


def print_stats(data, legend):
    data_col = data.T
    # Ignore the first column, which is Date
    for i in range(1, len(legend)):
        print(data_col[i])
        print("Average {} = {}".format(legend[i], np.mean(data_col[i])))
