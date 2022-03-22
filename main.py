import sys
import pandas as pd
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from sklearn import tree
import numpy as np
import matplotlib as mplt
import math
import matplotlib.pyplot as plt

nan = float('nan')

darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'

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

# Get WBC value from a given dataset
def getWBCData(dataset):
    rowNumber = 0
    while (dataset[rowNumber][0] != "HEMATOLOGY"):
        rowNumber += 1

    colNumber = 0
    # row is hematology
    while (dataset[rowNumber][colNumber] != "LOW"):
        colNumber += 1

    # we at LOW
    return dataset[rowNumber+3][colNumber]

#################################### Dashboard #######################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blubber")
        self.setFixedSize(QSize(700, 400))

        # LEFT SIDE:

        homeButton = QPushButton('Home')
        dataRangesButton = QPushButton('Data Ranges')
        aboutButton = QPushButton('About')

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(homeButton)
        leftLayout.addWidget(dataRangesButton)
        leftLayout.addWidget(aboutButton)
        leftLayout.addStretch()

        leftWidget = QWidget()
        leftWidget.setAutoFillBackground(True)
        leftWidget.setFixedWidth(200)
        leftWidget.setLayout(leftLayout)
        p = leftWidget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        leftWidget.setPalette(p)

        # RIGHT SIDE:

        inputLine = QLineEdit()
        inputLine.setFixedWidth(300)
        inputLine.setPlaceholderText('Input')

        importButton = QPushButton('Import')
        importButton.setAttribute

        outputLabel = QLabel()
        outputLabel.setText('Yes / No is the seals dead')

        saveButton = QPushButton('Save')

        imageLabel = QLabel()
        pic = QPixmap('fancyGraph.png').scaledToHeight(250)
        imageLabel.setPixmap(pic)

        rightLayout = QGridLayout()
        rightLayout.addWidget(inputLine, 0, 0)
        rightLayout.addWidget(importButton, 0, 1)
        rightLayout.addWidget(outputLabel, 1, 0)
        rightLayout.addWidget(saveButton, 1, 1)
        rightLayout.addWidget(imageLabel, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        rightWidget = QWidget()
        rightWidget.setAutoFillBackground(True)
        rightWidget.setLayout(rightLayout)
        q = rightWidget.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        rightWidget.setPalette(q)

        layout = QGridLayout()
        layout.addWidget(leftWidget, 0, 0)
        layout.addWidget(rightWidget, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

# app.exec()

# Load the data
wbcDataArr = np.array([])
labels = np.array([])

# look into regexp
# npthingArrivedSeals.shape[0]
for i in range(221, 300):
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
        if not (math.isnan(getWBCData(npthing))):
            wbcData = getWBCData(npthing)
            wbcDataArr = np.append(wbcDataArr, wbcData)
            labels = np.append(labels, getLabel(npthingArrivedSeals[i][2]))
    except:
        print("This file was not found - ", path)

wbcDecisionTree = tree.DecisionTreeClassifier()
wbcDecisionTree = wbcDecisionTree.fit(wbcDataArr.reshape(-1, 1), labels.reshape(-1, 1))
predictionArr = np.array([0])
# print(tree.export_text(wbcDecisionTree, show_weights=True))
plt.figure(figsize=(50, 50))

tree.plot_tree(wbcDecisionTree, filled=True)
plt.savefig(fname='treeOutput.png')
plt.show()
print(wbcDecisionTree.predict(predictionArr.reshape(1, -1)))