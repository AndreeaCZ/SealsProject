import pandas as pd
import os
import glob
import numpy as np
import sqlite3

from variables import DB_NAME, ARRIVED_SEALS_PATH, CLIENT_DATA_PATH, DIV

connection = sqlite3.connect(DB_NAME)
dataLabels = ["sealTag", "WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT", "Survival"]
startYear = 2014
folderPath = CLIENT_DATA_PATH
arrivedSeals = pd.read_excel(
    open(ARRIVED_SEALS_PATH, 'rb'),
    sheet_name='Arrived Seals', keep_default_na=False).to_numpy()
print(arrivedSeals.shape)


def get_values(nparray, sur, sealTag):
    try:
        if sur == "Released":
            surv = True
        else:
            surv = False

        colNumber = np.where(nparray == "LOW")[1][0]

        WBC = nparray[np.where(nparray == "WBC")[0][0]][colNumber]
        LYMF = nparray[np.where(nparray == "LYMF")[0][0]][colNumber]
        HCT = nparray[np.where(nparray == "HCT")[0][0]][colNumber]
        MCV = nparray[np.where(nparray == "MCV")[0][0]][colNumber]
        RBC = nparray[np.where(nparray == "RBC")[0][0]][colNumber]
        HGB = nparray[np.where(nparray == "HGB")[0][0]][colNumber]
        MCH = nparray[np.where(nparray == "MCH")[0][0]][colNumber]
        MCHC = nparray[np.where(nparray == "MCHC")[0][0]][colNumber]
        MPV = nparray[np.where(nparray == "MPV")[0][0]][colNumber]
        PLT = nparray[np.where(nparray == "PLT")[0][0]][colNumber]

        sealValues = [[sealTag, WBC, LYMF, HCT, MCV, RBC, HGB, MCH, MCHC, MPV, PLT, surv]]
        return sealValues
    except Exception as err1:
        print(Exception, err1)


def getSealSpecies(str):
    if str == "Phoca Vitulina":
        return "PV"
    if str == "Halichoerus Grypus":
        return "HG"


counter = 0

for i in range(221, arrivedSeals.shape[0]):
    try:
        tag = arrivedSeals[i][1]
        survival = arrivedSeals[i][2]
        sealSpecies = getSealSpecies(arrivedSeals[i][6])
        # get rid of T in tag ID
        sealTagWithoutT = tag[1:]
        if tag[1:3] == "20" or tag[1:3] == "21":
            filename = "20" + tag[1:3] + DIV + sealTagWithoutT + " " + sealSpecies + ".xlsx"
        else:
            filename = "20" + tag[1:3] + DIV + sealSpecies + sealTagWithoutT + ".xlsx"
        file = folderPath + DIV + filename
        allData = pd.read_excel(file, na_filter=True, engine='openpyxl').to_numpy()
        # print("Now extracting values from file: " + file)
        values = get_values(allData, survival, tag)
        sealData = pd.DataFrame(values, columns=dataLabels)
        counter += 1
        print(counter)
        sealData.to_sql(name='sealPredictionData', con=connection, if_exists='append', index=False)
    except Exception as err:
        print(Exception, err)

