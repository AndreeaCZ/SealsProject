import pandas as pd
from sklearn import tree
import numpy as np
import matplotlib as mplt
import math
import matplotlib.pyplot as plt

nan = float('nan')

# add path to arrived seals here
datasetArrivedSeals = pd.read_excel(open(r'/Users/andreeazelko/Documents/SoftwareEngineering/SealsProject/Arrived seals 2014-2021.xlsx', 'rb'), sheet_name='Arrived Seals')
npthingArrivedSeals = datasetArrivedSeals.to_numpy()
# add path to client data here
absolutePath = "/Users/andreeazelko/Documents/SoftwareEngineering/SealsProject/clientData/"

# Get the initials of the species
def getSealSpecies(str):
    if (str == "Phoca Vitulina"):
        return "PV"
    if (str == "Halichoerus Grypus"):
        return "HG"

# Get the label based on the string
# Right now - Everything but released is death so it's a 0
def getLabel(str):
    if (str == "Released"):
        return 1
    else:
        return 0


def getData(dataset, type, perc):
    colNumber = np.where(dataset == "LOW")[1][0]
    rows = np.where(dataset == type)[0]
    if perc:
        for i in rows:
            if dataset[i][1] == "%":
                rowNumber = i
                break
    else:
        for i in rows:
            if dataset[i][1] != "%":
                rowNumber = i
                break
    print("success", rowNumber, colNumber)
    return dataset[rowNumber][colNumber]


# Get WBC value from a given dataset
# def getWBCData(dataset):
#     colNumber = np.where( dataset == "LOW")[1][0]
#     rowNumber = np.where( dataset == "WBC")[0][0]
#     return dataset[rowNumber][colNumber]
#
# #units
# def getLymfData(dataset):
#     colNumber = np.where(dataset == "LOW")[1][0]
#     rows = np.where(dataset == "LYMF")[0]
#     for i in rows:
#         if dataset[i][1] != "%":
#             rowNumber = i
#             break
#     return dataset[rowNumber][colNumber]
#
#
# def getGranData(dataset):
#     colNumber = np.where(dataset == "LOW")[1][0]
#     rows = np.where(dataset == "GRAN")[0]
#     for i in rows:
#         if dataset[i][1] != "%":
#             rowNumber = i
#             break
#     return dataset[rowNumber][colNumber]


# Load the data
wbcDataArr = np.array([])
lymfDataArr = np.array([])
labels = np.array([])

# look into regexp
# npthingArrivedSeals.shape[0]
for i in range(221, npthingArrivedSeals.shape[0]):
    try:
        sealTag = npthingArrivedSeals[i][1]
        sealSpecies = getSealSpecies(npthingArrivedSeals[i][6])
        # get rid of T in tag ID
        sealTagWithoutT = sealTag[1:]
        if (sealTag[1:3] == "20" or sealTag[1:3] == "21"):
            filename = "20" + sealTag[1:3] + "/" + sealTagWithoutT + " " + sealSpecies + ".xlsx"
        else:
            filename = "20" + sealTag[1:3] + "/" + sealSpecies + sealTagWithoutT + ".xlsx"
        path = absolutePath + filename
        dataset = pd.read_excel(path)
        npthing = dataset.to_numpy()
        # check this out
        if not (math.isnan(getData(npthing, "WBC", False))):
            wbcData = getData(npthing, "WBC", False)
            wbcDataArr = np.append(wbcDataArr, wbcData)
            labels = np.append(labels, getLabel(npthingArrivedSeals[i][2]))
            if not (math.isnan(getData(npthing, "LYMF", False))):
                lymfDataNoPerc = getData(npthing, "LYMF", False)
                lymfDataArr = np.append(lymfDataArr, lymfDataNoPerc)
        else:
            print(path)
    except:
        print("This file was not found - ", path)

print(lymfDataArr)
wbcDecisionTree = tree.DecisionTreeClassifier()
wbcDecisionTree = wbcDecisionTree.fit(wbcDataArr.reshape(-1, 1), labels.reshape(-1, 1))
predictionArr = np.array([0])
# print(tree.export_text(wbcDecisionTree, show_weights=True))
plt.figure(figsize=(50, 50))

tree.plot_tree(wbcDecisionTree, filled=True)
plt.savefig(fname='treeOutput.png')
plt.show()
print(wbcDecisionTree.predict(predictionArr.reshape(1, -1)))