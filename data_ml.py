# EECS458 BioInfo
# TungHo Lin
# txl429
# This file employs ML algorithms to the datasets

import csv
import os
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plt
import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm


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
                aligned.append([np.float64(entry_1[2]), np.float64(entry_2[2])])
    return np.array(aligned)


def get_k_means_classifier(dataset, n_clusters=2):
    k_means = cluster.KMeans(n_clusters=n_clusters)
    k_means.fit(dataset)
    print("K-Means Clusters with k = {}".format(n_clusters))
    # print("K-Means Score: {}".format(k_means.score(dataset)))
    sorted_centers = list(k_means.cluster_centers_)
    sorted_centers.sort(key=lambda c: c[0])
    # for center in k_means.cluster_centers_:
    for center in sorted_centers:
        print("HR Sum: {}; Steps: {}; Ratio: {}".format(str(center[0])[:5], str(center[1])[:5]
              , str(center[0]/center[1])[:5]))
    return k_means


def get_knn_classifier(dataset, n_neighbors=1):
    print("K-Neighbors for k = {}:".format(n_neighbors))
    x_train = dataset[:, 0].reshape(-1, 1)
    y_train = dataset[:, 1]
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(x_train, y_train)
    # print("KNN Score: {}".format(knn.score(x_train, y_train)))
    return knn


def get_svm_classifier(dataset):
    svc = svm.SVC(kernel='rbf', C=1.0)
    x_train = dataset[:, 0].reshape(-1, 1)
    y_train = dataset[:, 1]
    svc.fit(x_train, y_train)
    # print("SVM Score: {}".format(svc.score(x_train, y_train)))
    return svc


def get_logreg_classifier(dataset):
    x_train = dataset[:, 0].reshape(-1, 1)
    y_train = dataset[:, 1]
    logreg = LogisticRegression(random_state=0)
    logreg.fit(x_train, y_train)
    # print("LogReg Score: {}".format(logreg.score(x_train, y_train)))
    return logreg


def plot_k_means_clusters(classifier, dataset, n_clusters=2):
    plt.figure(n_clusters-1)
    plt.xlabel('Hourly HeartRate Sum')
    plt.ylabel('Hourly Steps')
    plt.scatter(dataset[:, 0], dataset[:, 1], c=classifier.labels_, cmap='rainbow')
    plt.scatter(classifier.cluster_centers_[:, 0], classifier.cluster_centers_[:, 1], color='black')
    plt.title("KMeans with {} clusters".format(n_clusters))
    plt.show()


def predict_with_classifier(classifier, heartrates):
    results = []
    for hr in heartrates:
        predicted_steps = classifier.predict([[hr]])[0]
        print("HR Sum: {}; Predicted Steps: {}".format(hr, predicted_steps))
        results.append(predicted_steps)
    return results


def num_of_0_in_steps(steps_dataset):
    count = 0
    for entry in steps_dataset:
        if np.float(entry[2]) == 0.0:
            count += 1
    print("Number of ZERO entries: {}".format(count))
    return count


def remove_0_in_dataset(dataset):
    processed = []
    print("Removing ZERO entries in the dataset")
    for entry in dataset:
        if float(entry[2]) != float(0):
            processed.append(entry)
    print("Original Length: {}; Processed Length: {}".format(len(dataset), len(processed)))
    return processed


def main_hr_steps():
    # This line is giving a lot of FutureWarnings even when the entire array is np.float64
    # Will suppress it for now
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    months = ["march", "april"]
    examples_heartrates = np.array(["20000", "40000", "60000", "90000"]).astype(np.float64)
    hourly_heartrate = parse_attr("6962181067", "heartrate_hour_sum", months)
    hourly_steps = parse_attr("6962181067", "hourlySteps", months)
    num_of_0_in_steps(hourly_steps)

    # COMMENT THESE TWO LINES OUT IF YOU WANT TO USE THE FULL UNPROCESSED DATTASETS
    hourly_heartrate = remove_0_in_dataset(hourly_heartrate)
    hourly_steps = remove_0_in_dataset(hourly_steps)

    aligned = produce_aligned_dataset(hourly_heartrate, hourly_steps)
    print("Dataset Length: {}".format(len(aligned)))
    print("*** Logistic Regression ***")
    logreg = get_logreg_classifier(aligned)
    predict_with_classifier(logreg, examples_heartrates)
    print("*** Support Vector Machine ***")
    svc = get_svm_classifier(aligned)
    predict_with_classifier(svc, examples_heartrates)
    for k in range(2, 10):
        print("\n********K={}********".format(k))
        k_means = get_k_means_classifier(aligned, n_clusters=k)
        plot_k_means_clusters(k_means, aligned, n_clusters=k)
        knn = get_knn_classifier(aligned, n_neighbors=k)
        predict_with_classifier(knn, examples_heartrates)


# I originally used "calories" to compare it to heartrate
# but I realize it is a derived attribute so I switched over to using steps
# def main_hr_calories():
#     # This line is giving a lot of FutureWarnings even when the entire array is np.float64
#     # Will suppress it for now
#     import warnings
#     warnings.simplefilter(action='ignore', category=FutureWarning)
#
#     months = ["march", "april"]
#     examples_heartrates = np.array(["73", "75", "135", "151"]).astype(np.float64)
#     hourly_heartrate = parse_attr("6962181067", "heartrate_hour", months)
#     hourly_calorie = parse_attr("6962181067", "hourlyCalories", months)
#     aligned = produce_aligned_dataset(hourly_heartrate, hourly_calorie)
#     print("Dataset Length: {}".format(len(aligned)))
#     logreg = get_logreg_classifier(aligned)
#     predict_with_classifier(logreg, examples_heartrates)
#     svc = get_svm_classifier(aligned)
#     predict_with_classifier(svc, examples_heartrates)
#     knn = get_knn_classifier(aligned)
#     predict_with_classifier(knn, examples_heartrates)
    # for k in range(2, 10):
    #     print("\n********K={}********".format(k))
    #     k_means = get_k_means_classifier(aligned, n_clusters=k)
    #     plot_k_means_clusters(k_means, aligned, n_clusters=k)
    #     knn = get_knn_classifier(aligned, n_neighbors=k)
    #     predict_with_classifier(knn, examples_heartrates)


if __name__ == '__main__':
    # main_hr_calories()
    main_hr_steps()
