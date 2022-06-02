import sqlite3

import numpy as np
from PyQt6.QtGui import QPalette, QColor

from GUI.utils import *
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *
from variables import DB_PATH

########################################################################################################################
# Represents the window that lets the user see seal data
########################################################################################################################

dataLabels = ["sealTag", "WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT", "Survival", "Sex", "Species"]


class GetSealDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Get seal data")
        self.setFixedSize(QSize(700, 400))

        # Creating elements:
        self.sealTag_input_line = QLineEdit()
        self.sealTag_label = QLabel()
        self.output_label = QLabel()
        self.getSealData_button = QPushButton('Get seal data')

        # Setting widget properties:
        self.setLayout(self.set_elements())
        self.setAutoFillBackground(True)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)

    def set_elements(self):
        """
        Sets the elements of the window
        :return: the layout of the window
        """
        # Setting the elements:
        self.sealTag_label.setText("Enter a unique seal tag to retrieve its details from the database")
        self.getSealData_button.clicked.connect(self.get_seal_data)
        # Adding the elements to the layout:
        layout = QGridLayout()
        layout.addWidget(self.sealTag_label)
        layout.addWidget(self.sealTag_input_line)
        layout.addWidget(self.output_label)
        layout.addWidget(self.getSealData_button)
        return layout

    # presents the seal data to the output panel
    def show_seal_data(self, sealData):
        s = ""
        for i in range(11):
            s = s + dataLabels[i] + " - " + sealData[i] + "\n"
        s = s + dataLabels[11] + " - " + get_survival_str_from_int(int(sealData[11])) + "\n"
        s = s + dataLabels[12] + " - " + get_sex_str_from_int(int(sealData[12])) + "\n"
        s = s + dataLabels[13] + " - " + get_seal_species_str_from_int(int(sealData[13])) + "\n"
        self.output_label.setText(s)

    # retrieves the data of the seal with a seal tag
    # if the result is zero, there´s a problem when taking the input
    def get_seal_data(self):
        sealTag = self.sealTag_input_line.text()
        connection = sqlite3.connect(DB_PATH)  # create a database for model training data
        c = connection.cursor()
        try:
            sql = """SELECT * FROM sealPredictionData WHERE sealTag = ?"""
            c.execute(sql, (sealTag,))
            sealData = c.fetchone()
            npSealData = np.array(sealData)
            self.show_seal_data(npSealData)
        except:
            pop_message_box("Something went wrong. Ensure that you've provided the seal tag of a seal present in the database.")
            self.output_label.setText("")
        connection.close()
