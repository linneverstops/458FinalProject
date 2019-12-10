import csv
import os
from sklearn import cluster, datasets
import numpy as np
import matplotlib.pyplot as plt
import datetime

def find_global_mean(attr, months):
    pass


def find_monthly_mean(attr, month):
    pass


def parse_attr(user_id, attr, months):
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
    return dataset


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


def produce_aligned_dataset(dataset_1, dataset_2):
    aligned = []
    for entry_1 in dataset_1:
        datetime_1_str = entry_1[1]
        datetime_1 = datetime.datetime.strptime(datetime_1_str, "%m/%d/%Y %H:%M:%S %p")
        for entry_2 in dataset_2:
            datetime_2_str = entry_2[1]
            datetime_2 = datetime.datetime.strptime(datetime_2_str, "%m/%d/%Y %H:%M:%S %p")
            same_time = (datetime_2 - datetime_1).total_seconds() == 0.0
            if same_time:
                aligned.append([entry_1[2], entry_2[2]])
    return aligned


def plot_kmeans_clusters(dataset):
    k_means = cluster.KMeans(n_clusters=2)
    k_means.fit(dataset)
    plt.figure(1)
    plt.xticks([])
    plt.yticks([])
    plt.scatter(dataset[:, 0], dataset[:, 1], c=k_means.labels_, cmap='rainbow')
    plt.scatter(k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1], color='black')
    plt.legend()
    plt.show()


def main():
    # ids = get_user_ids()
    # attrs = get_attrs()
    months = ["march", "april"]
    hourly_calorie = parse_attr("6962181067", "hourlyCalories", months)
    hourly_heartrate = parse_attr("6962181067", "heartrate_hour", months)
    aligned = produce_aligned_dataset(hourly_calorie, hourly_heartrate)
    # print(aligned)
    print(len(aligned))
    # input = np.array(list(map(list, zip(*dataset))))
    plot_kmeans_clusters(np.array(aligned))


if __name__ == '__main__':
    main()
