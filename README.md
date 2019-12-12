# 458FinalProject
Repo for my EECS458 BioInformatics Final Project

Fitbit dataset downloaded from: \
https://zenodo.org/record/53894

Dataset:\
-2 months of fitbit data sourced from 30 participants

Fields of interest:\
-heartrate_seconds (will be converted to heartrate_hour)\
-hourly_calories\
-hourly_steps\

Idea:\
-parse the collective dataset into different users\
-preprocess data to match the timestamp and values\
-Use (mainly) K-Means Clustering and KNN to classify samples\
-identify abnormalities/outliers\
-Calculate a new sample's heartrate/steps ratio\