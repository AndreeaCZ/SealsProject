import sqlite3

import numpy as np
import pandas as pd

dataLabels = ["sealTag", "WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT", "Survival", "Sex", "Species"]
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *
from variables import DB_PATH

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

    # returns the species from the integer representation
    def getSealSpeciesStrFromInt(self, x):
        if x == '0':
            return "Phoca Vitulina"
        if x == '1':
            return "Halichoerus Grypus"

    # returns the sex from the integer representation
    def getSexStrFromInt(self, x):
        if x == '0':
            return "Female"
        if x == '1':
            return "Male"

    # returns the survival from the integer representation
    def getSurvivalStrFromInt(self, x):
        if x == '0':
            return "Not released"
        if x == '1':
            return "Released"

        # presents the seal data to the output panel
    def showSealData(self, sealData):
        str = ""
        for i in range(11):
            str = str + dataLabels[i] + " - " + sealData[i] + "\n"
        str = str + dataLabels[11] + " - " + self.getSurvivalStrFromInt(sealData[11]) + "\n"
        str = str + dataLabels[12] + " - " + self.getSexStrFromInt(sealData[12]) + "\n"
        str = str + dataLabels[13] + " - " + self.getSealSpeciesStrFromInt(sealData[13]) + "\n"
        self.output_label.setText(str)

    # retrieves the data of the seal with a seal tag
    # if the result is zero, there´s a problem when taking the input
    def get_Seal_Data(self):
        sealTag = self.sealTag_input_line.text()
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
            self.output_label.setText("")
        connection.close()