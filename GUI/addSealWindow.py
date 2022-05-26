import sqlite3
import pandas as pd

from GUI.predictionWindow import getSexInt, getSealSpeciesInt
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *

from Utilities.excelManipulation import get_blood_test_values
from variables import DB_NAME, DB_PATH

# Represents the window that lets the user add a seal to the database
class AddSealWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add a seal")
        self.setFixedSize(QSize(700, 400))

        # Creating elements:
        self.sealTag_input_line = QLineEdit()
        self.sealTag_label = QLabel()
        self.sealTag_label.setText("Enter a unique seal tag")
        self.addSeal_button = QPushButton('Add Seal')
        self.addSeal_button.clicked.connect(self.add_Seal)

        # Creating import sub fields
        self.combo1 = QComboBox()
        self.combo1.addItem("Female")
        self.combo1.addItem("Male")
        self.combo2 = QComboBox()
        self.combo2.addItem("Phoca Vitulina")
        self.combo2.addItem("Halichoerus Grypus")
        self.combo3 = QComboBox()
        self.combo3.addItem("Released")
        self.combo3.addItem("Not released")

        layout = QGridLayout()
        layout.addWidget(self.combo1)
        layout.addWidget(self.combo2)
        layout.addWidget(self.combo3)
        layout.addWidget(self.sealTag_label)
        layout.addWidget(self.sealTag_input_line)
        layout.addWidget(self.addSeal_button)
        self.setLayout(layout)

    # pops open a message box with the passed str as the message
    def popMessageBox(self, str):
        msgBox = QMessageBox()
        msgBox.setText(str)
        msgBox.exec()

    # if the result is zero, there´s a problem when taking the input
    def add_Seal(self):
        import_path_null = False;
        sealTag = self.sealTag_input_line.text()
        if not (sealTag == ""):
            import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
            if (import_path == ""):
                import_path_null = True;
            if not import_path_null:
                self.addToDatabase(import_path, sealTag)
        else:
            self.popMessageBox("Provide a unique seal tag ID")

    # adds a seal to the database
    def addToDatabase(self, file, sealTag):
        sex1 = self.combo1.currentText()
        species1 = self.combo2.currentText()
        Sex = getSexInt(sex1)
        Species = getSealSpeciesInt(species1)
        Surv = self.combo3.currentText()
        if (Surv == "Released"):
            Survival = 1
        else:
            Survival = 0
        data = pd.read_excel(file, na_filter=True, engine='openpyxl').to_numpy()
        blood_values = get_blood_test_values(data,["WBC", "LYMF", "HCT", "MCV", "RBC", "HGB", "MCH", "MCHC", "MPV","PLT"])
        if not (blood_values == 0):
            WBC = blood_values[0]
            LYMF = blood_values[1]
            HCT = blood_values[2]
            MCV = blood_values[3]
            RBC = blood_values[4]
            HGB = blood_values[5]
            MCH = blood_values[6]
            MCHC = blood_values[7]
            MPV = blood_values[8]
            PLT = blood_values[9]
            connection = sqlite3.connect(DB_PATH)  # create a database for model training data
            c = connection.cursor()
            try:
                sql = "INSERT INTO sealPredictionData(sealTag, WBC, LYMF, HCT, MCV, RBC, HGB, MCH, MCHC, MPV, PLT, Survival, Sex, Species) VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?);"
                c.execute(sql, (sealTag, WBC, LYMF, HCT, MCV, RBC, HGB, MCH, MCHC, MPV, PLT, Survival, Sex, Species));
                connection.commit()
                self.popMessageBox("Successfully added seal to the database")
            except:
                self.popMessageBox("Something went wrong. Ensure that the seal tag is unique.")
            connection.close()