# EECS458 BioInfo
# TungHo Lin
# txl429
# This file will take a merged datafile and outputs them into individual files
import os
import sys
import csv
import datetime
import numpy as np


def convert_heartrate_secs_to_hour(months):
    for month in months:
        dirpath = "individuals/{}_{}".format(month, "heartrate_seconds")
        new_dirpath = "individuals/{}_{}".format(month, "heartrate_hour")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                id_attr = file.replace("_seconds.csv", "")
                filepath = "{}/{}".format(dirpath, file)
                new_filepath = "{}/{}_hour.csv".format(new_dirpath, id_attr)
                with open(filepath, newline='') as r:
                    seconds_data = []
                    reader = csv.reader(r, delimiter=',')
                    for row in reader:
                        seconds_data.append(row)
                    hour_data = __convert_seconds_data_to_hour(seconds_data)
                    with open(new_filepath, 'w+', newline='') as w:
                        writer = csv.writer(w, delimiter=',')
                        for row in hour_data:
                            writer.writerow(row)


def __convert_seconds_data_to_hour(seconds_data):
    hour_data = []
    buffer = []
    user_id = seconds_data[1][0]
    is_legend_row = True
    for row in seconds_data:
        if is_legend_row:
            is_legend_row = False
            continue
        datetime_str = row[1]
        cur_datetime = datetime.datetime.strptime(datetime_str, "%m/%d/%Y %I:%M:%S %p")
        if len(buffer) > 0:
            start_datetime = datetime.datetime.strptime(buffer[0][1], "%m/%d/%Y %I:%M:%S %p")
            time_diff_in_s = (cur_datetime - start_datetime).total_seconds()
            hours = divmod(time_diff_in_s, 3600)[0]
            if np.abs(hours) >= 1.0:
                # start_datetime.
                # print(np.abs(hours))
                # retrieve the heartrate
                # use the max instead of the mean
                # mean_hour_hr = str(np.mean(np.array(buffer)[:, 2].astype(np.float)))[:5]
                mean_hour_hr = str(np.max(np.array(buffer)[:, 2].astype(np.float)))[:5]
                corrected_datetime = start_datetime.replace(minute=0, second=0).strftime("%m/%d/%Y %I:%M:%S %p")
                hour_data.append([user_id, corrected_datetime, mean_hour_hr])
                buffer = []
            else:
                buffer.append(row)
        else:
            buffer.append(row)
    return hour_data


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
                attr = file.replace("_merged.csv", "")
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


def main2():
    convert_heartrate_secs_to_hour(["march", "april"])


if __name__ == '__main__':
    # main()
    main2()
