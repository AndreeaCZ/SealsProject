import pandas as pd
from sklearn import tree
import numpy as np
import math
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from dataParser import get_data

nan = float('nan')

# add path to arrived seals here
datasetArrivedSeals = pd.read_excel(
    open(r'/Users/andreeazelko/Documents/SoftwareEngineering/SealsProject/Arrived seals 2014-2021.xlsx', 'rb'),
    sheet_name='Arrived Seals')
npthingArrivedSeals = datasetArrivedSeals.to_numpy()
# add path to client data here
absolutePath = r"/Users/andreeazelko/Documents/SoftwareEngineering/SealsProject/clientData"


# Get the initials of the species
def getSealSpecies(str):
    if str == "Phoca Vitulina":
        return "PV"
    if str == "Halichoerus Grypus":
        return "HG"


# Get the label based on the string
# Right now - Everything but released is death so it's a 0
def getLabel(str):
    if (str == "Released"):
        return 1
    else:
        return 0


# Load the data
trainingArr = np.array([[]])
wbcDataArr = np.array([])
lymfDataArr = np.array([])
granDataArr = np.array([])
midDataArr = np.array([])
lymfDataArrPerc = np.array([])
granDataArrPerc = np.array([])
midDataArrPerc = np.array([])
# Data not loaded yet
hctDataArr = np.array([])
mcvDataArr = np.array([])
rbcDataArr = np.array([])
hgbDataArr = np.array([])
mchDataArr = np.array([])
mchcDataArr = np.array([])
# rdwDataArrPerc = np.array([]) # additional data not loaded yet
# mpvDataArr = np.array([]) # additional data not loaded yet
pltDataArr = np.array([])
labels = np.array([])

# [[seal1wbc, seal1lymf],[seal2wbc, seal2lymf],...]
# look into regexp
# npthingArrivedSeals.shape[0]
for i in range(221, npthingArrivedSeals.shape[0]):
    try:
        sealTag = npthingArrivedSeals[i][1]
        sealSpecies = getSealSpecies(npthingArrivedSeals[i][6])
        # get rid of T in tag ID
        sealTagWithoutT = sealTag[1:]
        if sealTag[1:3] == "20" or sealTag[1:3] == "21":
            filename = "20" + sealTag[1:3] + "/" + sealTagWithoutT + " " + sealSpecies + ".xlsx"
        else:
            filename = "20" + sealTag[1:3] + "/" + sealSpecies + sealTagWithoutT + ".xlsx"
        path = absolutePath + "/" + filename
        dataset = pd.read_excel(path)
        ExcelSealData = dataset.to_numpy()
        sealData = np.array([[0] * 2] * 1)
        # check this out

        ################################################################################################################
        # or math.isnan(get_data(ExcelSealData, "RDW", True)) or math.isnan(get_data(ExcelSealData, "MPV", False))
        # the ones above crash the program
        ################################################################################################################
        if not (math.isnan(get_data(ExcelSealData, "WBC", False)) or math.isnan(get_data(ExcelSealData, "LYMF", False))
                or math.isnan(get_data(ExcelSealData, "LYMF", True)) or math.isnan(
                    get_data(ExcelSealData, "GRAN", False))
                or math.isnan(get_data(ExcelSealData, "GRAN", True)) or math.isnan(
                    get_data(ExcelSealData, "MID", False))
                or math.isnan(get_data(ExcelSealData, "MID", True)) or math.isnan(get_data(ExcelSealData, "HCT", False))
                or math.isnan(get_data(ExcelSealData, "MCV", False)) or math.isnan(
                    get_data(ExcelSealData, "RBC", False))
                or math.isnan(get_data(ExcelSealData, "HGB", False)) or math.isnan(
                    get_data(ExcelSealData, "MCH", False))
                or math.isnan(get_data(ExcelSealData, "MCHC", False)) or math.isnan(
                    get_data(ExcelSealData, "PLT", False))
        ):

            labels = np.append(labels, getLabel(npthingArrivedSeals[i][2]))
            wbcDataArr = np.append(wbcDataArr, get_data(ExcelSealData, "WBC", False))
            lymfDataArr = np.append(lymfDataArr, get_data(ExcelSealData, "LYMF", False))
            granDataArr = np.append(granDataArr, get_data(ExcelSealData, "GRAN", False))
            midDataArr = np.append(midDataArr, get_data(ExcelSealData, "MID", False))
            lymfDataArrPerc = np.append(lymfDataArrPerc, get_data(ExcelSealData, "LYMF", True))
            granDataArrPerc = np.append(granDataArrPerc, get_data(ExcelSealData, "GRAN", True))
            midDataArrPerc = np.append(midDataArrPerc, get_data(ExcelSealData, "MID", True))
            hctDataArr = np.append(hctDataArr, get_data(ExcelSealData, "HCT", False))
            mcvDataArr = np.append(mcvDataArr, get_data(ExcelSealData, "MCV", False))
            rbcDataArr = np.append(rbcDataArr, get_data(ExcelSealData, "RBC", False))
            hgbDataArr = np.append(hgbDataArr, get_data(ExcelSealData, "HGB", False))
            mchDataArr = np.append(mchDataArr, get_data(ExcelSealData, "MCH", False))
            mchcDataArr = np.append(mchcDataArr, get_data(ExcelSealData, "MCHC", False))
            # rdwDataArrPerc = np.append(rdwDataArrPerc, get_data(ExcelSealData, "RDW", True)) # additional data not appended yet
            # mpvDataArr = np.append(mpvDataArr, get_data(ExcelSealData, "MPV", False)) # additional data not appended yet
            pltDataArr = np.append(pltDataArr, get_data(ExcelSealData, "PLT", False))
        else:
            print(path)
    except:
        print("This file was not found - ", path)

trainingArr = np.vstack((wbcDataArr, lymfDataArr, lymfDataArrPerc)).T
sealTrain, sealTest = train_test_split(trainingArr, test_size=0.3, random_state=42)
trainLabel, testLabel = train_test_split(labels, test_size=0.3, random_state=42)
SealDecisionTree = tree.DecisionTreeClassifier()
SealDecisionTree = SealDecisionTree.fit(sealTrain, trainLabel.reshape(-1, 1))
predictions = SealDecisionTree.predict(sealTest)
accuracy = accuracy_score(testLabel, predictions)
print(accuracy)

# for printing / showing the decision tree
# plt.figure(figsize=(50, 50))
# tree.plot_tree(SealDecisionTree, filled=True)
# plt.savefig(fname='treeOutput.png')
# plt.show()

predictionArr = np.array([11.5, 1.5, 13.1])
print(SealDecisionTree.predict(predictionArr.reshape(1, -1)))

# joblib.dump(SealDecisionTree, 'SealDecisionTree.pkl')
