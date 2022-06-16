import sqlite3

import pandas as pd
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QGridLayout, QLineEdit, QLabel, QPushButton, QComboBox, QWidget, QFileDialog

from GUI.predictionWindow import get_sex_int, get_seal_species_int
from GUI.utils import lightgray, pop_message_box
from Utilities.excelManipulation import get_blood_test_values
from variables import DB_PATH


########################################################################################################################
# Represents the window that lets the user add a seal to the database
########################################################################################################################


class AddSealWindow(QWidget):
    def __init__(self, dashboard):
        super().__init__()
        self.setWindowTitle("Add a seal")
        self.setFixedSize(QSize(700, 400))

        # close home page
        self.dashboard = dashboard
        dashboard.close()

        # Creating elements:
        self.sealTag_input_line = QLineEdit()
        self.sealTag_label = QLabel()
        self.addSeal_button = QPushButton('Add Seal')
        self.infoLabel1 = QLabel('Please select sex, species and release status:')

        # Creating import subfields
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.combo3 = QComboBox()

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
        self.sealTag_label.setText("Enter a unique seal tag")
        self.addSeal_button.clicked.connect(self.add_seal)
        self.home_button.clicked.connect(self.go_to_home)
        self.combo1.addItem("Female")
        self.combo1.addItem("Male")
        self.combo2.addItem("Phoca Vitulina")
        self.combo2.addItem("Halichoerus Grypus")
        self.combo3.addItem("Released")
        self.combo3.addItem("Not released")

        # Adding the elements to the layout:
        layout = QGridLayout()
        layout.addWidget(self.infoLabel1, 0, 0)
        layout.addWidget(self.combo1, 1, 0)
        layout.addWidget(self.combo2, 2, 0)
        layout.addWidget(self.combo3, 3, 0)
        layout.setRowMinimumHeight(4, 40)
        layout.addWidget(self.sealTag_label, 5, 0)
        layout.addWidget(self.sealTag_input_line, 6, 0)
        layout.addWidget(self.addSeal_button, 7, 0)
        layout.addWidget(self.home_button, 8, 0)
        layout.setRowMinimumHeight(8, 70)
        return layout

    def go_to_home(self):
        """
        re-opens the dashboard and closes the current window
        """
        self.dashboard.show()
        self.close()

    def add_seal(self):
        """
        main function for adding a seal
        """
        import_path_null = False
        seal_tag = self.sealTag_input_line.text()
        if seal_tag != "":
            import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
            if import_path == "":
                import_path_null = True
            if not import_path_null:
                self.add_to_database(import_path, seal_tag)
        else:
            pop_message_box("Provide a unique seal tag ID")

    def add_to_database(self, file, seal_tag):
        """
        adds a seal to the database by extracting the seal data from the file
        :param file: the file path of seal data file
        :param seal_tag: the seal tag of the seal
        """
        sex_str = self.combo1.currentText()
        species_str = self.combo2.currentText()
        sex = get_sex_int(sex_str)
        species = get_seal_species_int(species_str)
        surv = self.combo3.currentText()
        if surv == "Released":
            survival = 1
        else:
            survival = 0
        data = pd.read_excel(file, na_filter=True, engine='openpyxl').to_numpy()
        blood_values = get_blood_test_values(data,
                                             ["WBC", "LYMF", "GRAN", "MID", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"])
        if blood_values != 0:
            WBC = blood_values[0]
            LYMF = blood_values[1]
            GRAN = blood_values[2]
            MID = blood_values[3]
            HCT = blood_values[4]
            MCV = blood_values[5]
            RBC = blood_values[6]
            HGB = blood_values[7]
            MCH = blood_values[8]
            MCHC = blood_values[9]
            MPV = blood_values[10]
            PLT = blood_values[11]
            connection = sqlite3.connect(DB_PATH)  
            c = connection.cursor()
            try:
                sql = "INSERT INTO sealPredictionData(sealTag, WBC, LYMF, GRAN, MID, HCT, MCV, RBC, HGB, MCH, MCHC, MPV, PLT, Survival, Sex, Species) VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                c.execute(sql, (seal_tag, WBC, LYMF, GRAN, MID, HCT, MCV, RBC, HGB, MCH, MCHC, MPV, PLT, survival, sex, species))
                connection.commit()
                pop_message_box("Successfully added seal to the database")
            except NameError:
                pop_message_box("Something went wrong. Ensure that the seal tag is unique.")
            connection.close()
