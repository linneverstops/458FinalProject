# EECS458 BioInfo
# TungHo Lin
# txl429
# This file is intended to be run and it should unmerge all data and run data analysis on it

import data_parser
import data_ml


def main():
    data_parser.main()
    data_ml.main_hr_steps()
    return


if __name__ == '__main__':
    main()
