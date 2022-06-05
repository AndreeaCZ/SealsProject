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

dataLabels = ["sealTag", "WBC", "LYMF", "GRAN", "MID", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT", "Survival", "Sex", "Species"]


class GetSealDataWindow(QWidget):
    def __init__(self, dashboard):
        super().__init__()
        self.setWindowTitle("Get seal data")
        self.setFixedSize(QSize(700, 500))
        # close the main window
        self.dashboard = dashboard
        dashboard.close()

        # Creating elements:
        self.sealTag_input_line = QLineEdit()
        self.sealTag_label = QLabel()
        self.output_label = QLabel()
        self.getSealData_button = QPushButton('Get seal data')

        # Creating a home button
        self.home_button = QPushButton('Home')

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
        self.home_button.clicked.connect(self.go_to_home)
        # Adding the elements to the layout:
        layout = QGridLayout()
        layout.addWidget(self.sealTag_label)
        layout.addWidget(self.sealTag_input_line)
        layout.addWidget(self.output_label)
        layout.addWidget(self.getSealData_button)
        layout.addWidget(self.home_button)
        return layout

    # re-opens the dashboard and closes the current window
    def go_to_home(self):
        self.dashboard.show()
        self.close()

    # presents the seal data to the output panel
    def show_seal_data(self, sealData):
        sealDataLen = len(sealData)
        s = ""
        for i in range(sealDataLen-3):
            s = s + dataLabels[i] + " - " + sealData[i] + "\n"
        s = s + dataLabels[sealDataLen-3] + " - " + get_survival_str_from_int(int(sealData[sealDataLen-3])) + "\n"
        s = s + dataLabels[sealDataLen-2] + " - " + get_sex_str_from_int(int(sealData[sealDataLen-2])) + "\n"
        s = s + dataLabels[sealDataLen-1] + " - " + get_seal_species_str_from_int(int(sealData[sealDataLen-1])) + "\n"
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
