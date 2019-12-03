# EECS458 BioInfo
# TungHo Lin
# txl429
# This file will take a merged datafile and outputs them into individual files
import os
import sys
import csv


def write_dict_to_csv(data_dict, month, attr):
    dirpath = "individuals/{}_{}".format(month, attr)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    for user_id in data_dict.keys():
        if user_id == "legend":
            continue
        filepath = "{}/{}_{}.csv".format(dirpath, user_id, attr)
        with open(filepath, 'w+', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data_dict["legend"])
            for value in data_dict[user_id]:
                writer.writerow(value)


def categorize_dataset_into_dict(filepath):
    data_dict = {}
    with open(filepath, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        index = 0
        for row in reader:
            if index == 0:
                data_dict["legend"] = row
            else:
                user_id = row[0]
                if user_id in data_dict:
                    data_dict[user_id].append(row)
                else:
                    data_dict[user_id] = [row]
            index += 1
    return data_dict


def unmerge_datasets_of_month(month):
    month = month.lower()
    print("Unmerging {}".format(month))
    for root, dirs, files in os.walk("datasets/{}/".format(month)):
        for file in files:
            if file.endswith(".csv"):
                attr = file.rstrip("_merged.csv")
                data_dict = categorize_dataset_into_dict("datasets/{}/{}".format(month, file))
                write_dict_to_csv(data_dict, month, attr)


def main():
    # Fields of interest:
    # -heart rate_seconds
    # -hourly_calories
    # -hourly_steps
    # -minute_sleep
    # -weight_log_info

    wd = os.getcwd()
    dirpath = wd + "/individuals"
    # create a directory 'output' if it doesn't exist yet
    if not os.path.exists(dirpath):
        print("New directory created under path: {}".format(dirpath))
        os.makedirs(dirpath)
    # import march datasets
    unmerge_datasets_of_month(month="march")
    # import april datasets
    unmerge_datasets_of_month(month="april")


if __name__ == '__main__':
    main()
