import sqlite3

import numpy as np
import pandas as pd

from GUI.predictionWindow import getSexInt, getSealSpeciesInt
dataLabels = ["sealTag", "WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT", "Survival", "Sex", "Species"]
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *

from Utilities.excelManipulation import get_blood_test_values
from variables import DB_PATH

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Represents the window that lets the user see seal data
class GetSealDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Get seal data")
        self.setFixedSize(QSize(700, 400))

        # Creating elements:
        self.sealTag_input_line = QLineEdit()
        self.sealTag_label = QLabel()
        self.output_label = QLabel()
        self.sealTag_label.setText("Enter a unique seal tag to retrieve its details from the database")
        self.getSealData_button = QPushButton('Get seal data')
        self.getSealData_button.clicked.connect(self.get_Seal_Data)

        layout = QGridLayout()
        layout.addWidget(self.sealTag_label)
        layout.addWidget(self.sealTag_input_line)
        layout.addWidget(self.output_label)
        layout.addWidget(self.getSealData_button)
        self.setLayout(layout)

    # pops open a message box with the passed str as the message
    def popMessageBox(self, str):
        msgBox = QMessageBox()
        msgBox.setText(str)
        msgBox.exec()

    # presents the seal data to the output panel
    def showSealData(self, sealData):
        str = ""
        for i in range(len(sealData)):
            str = str + dataLabels[i].format() + " - " + sealData[i] + "\n"
        self.output_label.setText(str)

    # 
    def getSealSpeciesStr(str):
        if str == "Phoca Vitulina":
            return "PV"
        if str == "Halichoerus Grypus":
            return "HG"

    # if the result is zero, there´s a problem when taking the input
    def get_Seal_Data(self):
        sealTag = self.sealTag_input_line.text()
        print(" this ")
        print(sealTag)
       # print(type(str(2)) == str)
        connection = sqlite3.connect(DB_PATH)  # create a database for model training data
        c = connection.cursor()
        try:
            sql = """SELECT * FROM sealPredictionData WHERE sealTag = ?"""
            c.execute(sql, (sealTag,))
            sealData = c.fetchone()
            npSealData = np.array(sealData)
            self.showSealData(npSealData)
        except:
            self.popMessageBox("Something went wrong. Ensure that you've provided the seal tag of a seal present in the database.")
        connection.close()