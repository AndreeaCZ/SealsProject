import pandas as pd
from sklearn import tree
import numpy as np
import math
import matplotlib.pyplot as plt
import joblib
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
lymfDataArrPerc = np.array([])
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
        if not (math.isnan(get_data(ExcelSealData, "WBC", False)) or math.isnan(
                get_data(ExcelSealData, "LYMF", False)) or math.isnan(get_data(ExcelSealData, "LYMF", True))):
            # sealData[0][0] = getData(npthing, "WBC", False)
            # sealData[0][1] = getData(npthing, "LYMF", False)
            wbcData = get_data(ExcelSealData, "WBC", False)
            wbcDataArr = np.append(wbcDataArr, wbcData)
            labels = np.append(labels, getLabel(npthingArrivedSeals[i][2]))

            lymfDataNoPerc = get_data(ExcelSealData, "LYMF", False)
            lymfDataArr = np.append(lymfDataArr, lymfDataNoPerc)

            lymfDataArrPerc = np.append(lymfDataArrPerc, get_data(ExcelSealData, "LYMF", True))
        else:
            print(path)
    except:
        print("This file was not found - ", path)

trainingArr = np.vstack((wbcDataArr, lymfDataArr, lymfDataArrPerc)).T
SealDecisionTree = tree.DecisionTreeClassifier()
SealDecisionTree = SealDecisionTree.fit(trainingArr, labels.reshape(-1, 1))

plt.figure(figsize=(50, 50))
tree.plot_tree(SealDecisionTree, filled=True)
plt.savefig(fname='treeOutput.png')
plt.show()

predictionArr = np.array([11.5, 1.5, 13.1])
print(SealDecisionTree.predict(predictionArr.reshape(1, -1)))

joblib.dump(SealDecisionTree, 'SealDecisionTree.pkl')
