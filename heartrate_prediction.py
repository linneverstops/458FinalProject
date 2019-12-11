from data_analysis import *
import numpy as np

def heartrate_prediction:
    model = {}



def main():
    months = ["march", "april"]
    examples_heartrates = np.array(["73", "75", "135", "151"]).astype(np.float64)
    hourly_heartrate = parse_attr("6962181067", "heartrate_hour", months)
    hourly_calorie = parse_attr("6962181067", "hourlyCalories", months)
    aligned = produce_aligned_dataset(hourly_heartrate, hourly_calorie)


if __name__ == '__main__':
    main()
