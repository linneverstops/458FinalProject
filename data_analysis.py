import csv
import os
from sklearn import cluster, datasets
import numpy as np
import matplotlib.pyplot as plt


def find_global_mean(attr, months):
    pass


def find_monthly_mean(attr, month):
    pass


def parse_attr_values_to_list(user_id, attr, months, value_at_col):
    list = []
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
                    list.append(row[value_at_col])
                    index += 1
            # print("Total num of lines: {}".format(index))
    return list


def get_user_ids():
    ids = []
    dirpath = "individuals/{}_{}".format("april", "minuteSleep")
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".csv"):
                id = file.replace("_minuteSleep.csv", "")
                ids.append(id)
    return ids


def get_attrs():
    attrs = []
    dirpath = "individuals"
    for root, dirs, files in os.walk(dirpath):
        for dir in dirs:
            if dir.startswith("april"):
                attr = dir.replace("april_", "")
                attrs.append(attr)
    return attrs


def plot_kmeans_clusters(input):
    k_means = cluster.KMeans(n_clusters=4)
    k_means.fit(input)
    plt.scatter(input[:, 0], input[:, 1], c=k_means.labels_, cmap='rainbow')
    plt.scatter(k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1], color='black')
    plt.show()


def main():
    ids = get_user_ids()
    attrs = get_attrs()
    months = ["march", "april"]
    dataset = []
    hour_calorie = parse_attr_values_to_list("6962181067", "hourlyCalories", months, 2)
    hour_heartrate = parse_attr_values_to_list("6962181067", "heartrate_hour", months, 2)
    dataset.append(hour_calorie)
    dataset.append(hour_heartrate)
    input = np.array(list(map(list, zip(*dataset))))
    plot_kmeans_clusters(input)



if __name__ == '__main__':
    main()
