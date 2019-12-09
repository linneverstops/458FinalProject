import csv
import os

import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def find_global_mean(attr, months):
    pass


def find_monthly_mean(attr, month):
    pass


def parse_attr_from_csv(user_id, attr, months):
    dataset = []
    for month in months:
        dirpath = "individuals/{}_{}".format(month, attr)
        if not os.path.exists(dirpath):
            print("ERROR: No csv is found. Make sure you have run single_user_parser.")
            return
        filepath = "{}/{}_{}.csv".format(dirpath, user_id, attr)
        index = 0
        with open(filepath, newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                # ignore the legend
                if index == 0:
                    index += 1
                    continue
                else:
                    dataset.append(row)
                    index += 1
            print("Total num of lines: {}".format(row))
    return dataset


def get_user_ids():
    ids = []
    dirpath = "individuals/{}_{}".format("april", "minuteSleep")
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".csv"):
                id = file.rstrip("_minuteSleep.csv")
                ids.append(id)
    return ids


def main():
    ids = get_user_ids()
    print(ids)


if __name__ == '__main__':
    main()
