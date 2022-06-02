import sqlite3

import pandas as pd

from GUI.utils import get_seal_species_int, get_sex_int
from Utilities.excelManipulation import get_blood_test_values
from variables import DB_NAME, ARRIVED_SEALS_PATH, CLIENT_DATA_PATH, DIV

#########################################################################################################################
# File used to import the client's Excel data into the app's database.
# Run file to fill the database with the data.
#########################################################################################################################

connection = sqlite3.connect(DB_NAME)
dataLabels = ["sealTag", "WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT", "Survival", "Sex",
              "Species"]
startYear = 2014
folderPath = CLIENT_DATA_PATH
arrivedSeals = pd.read_excel(
    open(ARRIVED_SEALS_PATH, 'rb'),
    sheet_name='Arrived Seals', keep_default_na=False).to_numpy()


def get_values(nparray, sur, sealTag, sealSex, species):
    """
    Extracts data from the database for a certain seal
    :param nparray: raw array from the excel file
    :param sur: the survival status of the seal
    :param sealTag: the seal's tag
    :param sealSex: the seal's sex
    :param species: the seal's species
    :return: list of the values for the seal
    """
    try:
        if sur == "Released":
            surv = True
        else:
            surv = False
        blood_values = get_blood_test_values(nparray,
                                             ["WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"])
        return [[sealTag] + blood_values + [surv] + [sealSex] + [species]]

    except Exception as err1:
        print(Exception, err1)


def get_seal_species_str(species):
    if species == "Phoca Vitulina":
        return "PV"
    if species == "Halichoerus Grypus":
        return "HG"


# Goes through the main Excel file and tries to get data about each seal and store it into the database
for i in range(221, arrivedSeals.shape[0]):
    try:
        tag = arrivedSeals[i][1]
        survival = arrivedSeals[i][2]
        sealSpecies = get_seal_species_str(arrivedSeals[i][6])
        sex = get_sex_int(arrivedSeals[i][7])
        # get rid of T in tag ID
        sealTagWithoutT = tag[1:]
        if tag[1:3] == "20" or tag[1:3] == "21":
            filename = "20" + tag[1:3] + DIV + sealTagWithoutT + " " + sealSpecies + ".xlsx"
        else:
            filename = "20" + tag[1:3] + DIV + sealSpecies + sealTagWithoutT + ".xlsx"
        file = folderPath + DIV + filename
        allData = pd.read_excel(file, na_filter=True, engine='openpyxl').to_numpy()
        values = get_values(allData, survival, tag, sex, get_seal_species_int(arrivedSeals[i][6]))
        if not (values == 0):
            sealData = pd.DataFrame(values, columns=dataLabels)
            sealData.to_sql(name='sealPredictionData', con=connection, if_exists='append', index=False)
    except Exception as err:
        print(Exception, err)
