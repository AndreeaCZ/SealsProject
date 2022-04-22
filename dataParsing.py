import pandas as pd
import os
import glob

sealData = pd.DataFrame() # create empty dataframe
readData = ["Species:", "Rhb. number:", "WBC", "LYMF", "MID", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]
# create list of data string names for the search

startYear = 2014
path = r"/Users/dobrematei/Desktop/University of Groningen/Software Engineering/SealsProject/sealData"
for i in range(0, 7):
    path = path + '/' + str((startYear + i))  # iterate through each year's folder
    print(path)  # check if the path is correct
    csv_files = glob.glob(os.path.join(path, "*.xlsx"))  # get all the excel files in the folder
    for file in csv_files:
    # retrieve seal tag, data and state (dead or alive)
    # seal tag and id come from column C where
    try:

        for r in readData:
            sealData = pd.concat([sealData, pd.read_excel(file, na_filter=True, na_values=['NA'], usecols='E',
                                                          engine='openpyxl').T])
        # read the excel file, skip rows based on logic function, only read 15 rows after that,only read the
        # column E and handle NA values
    except:
        print("Error in file: " + file)
    path = r"/Users/dobrematei/Desktop/University of Groningen/Software Engineering/SealsProject/sealData"  # reset the path
sealData.to_sql('sealPredictionData', if_exists='append')  # create append the dataframe to the main database
