import csv
import os
from sklearn import cluster, datasets
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
            print("ERROR: path {} does not exist".format(dirpath))
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
            print("Total num of lines: {}".format(index))
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


def get_attrs():
    attrs = []
    dirpath = "individuals"
    for root, dirs, files in os.walk(dirpath):
        for dir in dirs:
            if dir.startswith("april"):
                attr = dir.lstrip("april_")
                attrs.append(attr)
    return attrs


def main():
    ids = get_user_ids()
    # print(ids)
    attrs = get_attrs()
    # print(attrs)
    months = ["march", "april"]
    minsleep_dataset = parse_attr_from_csv(ids[0], "minuteSleep", months)
    # print(minsleep_dataset)
    k_means = cluster.KMeans(n_clusters=2)
    k_means.fit(minsleep_dataset)
    print(k_means.labels_[::10])


if __name__ == '__main__':
    main()
