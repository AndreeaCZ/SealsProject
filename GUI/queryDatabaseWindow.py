import sqlite3

import numpy as np
import pandas as pd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QCheckBox, QComboBox, QGridLayout, QFileDialog, QLabel
import datetime

from GUI.utils import lightgray, pop_message_box
from variables import DB_PATH, DIV


class QueryDatabaseWindow(QWidget):
    def __init__(self, dashboard):
        super().__init__()
        self.sealData = None
        self.setWindowTitle("Query the database")
        self.setFixedSize(QSize(900, 600))

        # close the main dashboard
        self.dashboard = dashboard
        dashboard.close()

        # Creating a home button
        self.home_button = QPushButton('Home')

        # Creating labels:
        self.infoLabel1 = QLabel('Please enter ranges for the following values:')
        self.infoLabel2 = QLabel('Please select additional fields:')
        self.infoLabel3 = QLabel('Please enter a file name and press Get the subsets so see results')

        # Blood values:
        self.minWBC = QLineEdit()
        self.maxWBC = QLineEdit()
        self.minLYMF = QLineEdit()
        self.maxLYMF = QLineEdit()
        self.minGRAN = QLineEdit()
        self.maxGRAN = QLineEdit()
        self.minMID = QLineEdit()
        self.maxMID = QLineEdit()
        self.minHCT = QLineEdit()
        self.maxHCT = QLineEdit()
        self.minMCV = QLineEdit()
        self.maxMCV = QLineEdit()
        self.minRBC = QLineEdit()
        self.maxRBC = QLineEdit()
        self.minHGB = QLineEdit()
        self.maxHGB = QLineEdit()
        self.minMCH = QLineEdit()
        self.maxMCH = QLineEdit()
        self.minMCHC = QLineEdit()
        self.maxMCHC = QLineEdit()
        self.minMPV = QLineEdit()
        self.maxMPV = QLineEdit()
        self.minPLT = QLineEdit()
        self.maxPLT = QLineEdit()

        # Survival:
        self.survY = QCheckBox("Released")
        self.survN = QCheckBox("Not released")

        # Sex:
        self.sexF = QCheckBox("Female")
        self.sexM = QCheckBox("Male")

        # Species:
        self.speciesPV = QCheckBox("Phoca Vitulina")
        self.speciesHG = QCheckBox("Halichoerus Grypus")

        # Year:
        self.minYear = QLineEdit()
        self.maxYear = QLineEdit()

        # order by
        self.orderBy = QComboBox()

        # order by ascending or descending
        self.order = QComboBox()

        # execute query
        self.executeButton = QPushButton('Get the subsets')

        # filename
        self.fileName = QLineEdit()

        # Set widget properties:
        self.setLayout(self.set_elements())
        self.setAutoFillBackground(True)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)

    # re-opens the dashboard and closes the current window
    def go_to_home(self):
        self.dashboard.show()
        self.close()

    def get_min_tag_for_year(self, year):
        """
        Rewrite minimum year in the form of sealtag
        :param year: the mininum year
        :return the smallest seal tag represented by the year
        """
        string = "T" + str(year % 100) + "-000"
        return string

    def get_max_tag_for_year(self, year):
        """
        Rewrite maximum year in the form of sealtag
        :param year: the maximum year
        :return the greatest seal tag represented by the year
        """
        string = "T" + str(year % 100) + "-999"
        return string

    def get_excluded_value(self, input1, input2):
        """
        Get the excluded value based on the inputs
        :param input1: a boolean value
        :param input2: a boolean value
        :return: the number to be excluded in the sql query
        """
        if input1 and input2:
            return 2
        elif input1:
            return 1
        elif input2:
            return 0
        else:
            return 2

    def get_year(self):
        """
        Sets default values for min and max year
        :return minYear: the smallest seal tag possible for the min year
        :return maxYear: the largest seal tag possible for the max year
        """
        if (self.minYear.text() == ""):
            minYear = 2014
        else:
            minYear = int(float(self.minYear.text()))

        if (self.maxYear.text() == ""):
            currentDateTime = datetime.datetime.now()
            date = currentDateTime.date()
            maxYear = int(date.strftime("%Y"))
        else:
            maxYear = int(float(self.maxYear.text()))

        minStr = self.get_min_tag_for_year(minYear)
        maxStr = self.get_max_tag_for_year(maxYear)
        return minStr, maxStr

    def save_data(self, df):
        """
        Saves the data from the dataframe passed into an excel file
        :param df: the dataframe to be saved
        """
        fileName = self.fileName.text()
        if fileName == "":
            pop_message_box("Please enter a file name first.")
        else:
            import_path = QFileDialog.getExistingDirectoryUrl().path()
            if not (import_path == ""):
                import_path = import_path + DIV + fileName + '.xlsx'
                df.to_excel(import_path)
                # pops a message box
                pop_message_box("Subsets saved successfully")
            self.fileName.setText("")

    def execute_query(self):
        """
        Execute the query
        """
        # get blood values from text fields
        self.set_default_values()
        noNumInput = False
        try:
            minWBC = float(self.minWBC.text())
            maxWBC = float(self.maxWBC.text())
            minLYMF = float(self.minLYMF.text())
            maxLYMF = float(self.maxLYMF.text())
            minGRAN = float(self.minGRAN.text())
            maxGRAN = float(self.maxGRAN.text())
            minMID = float(self.minMID.text())
            maxMID = float(self.maxMID.text())
            minHCT = float(self.minHCT.text())
            maxHCT = float(self.maxHCT.text())
            minMCV = float(self.minMCV.text())
            maxMCV = float(self.maxMCV.text())
            minRBC = float(self.minRBC.text())
            maxRBC = float(self.maxRBC.text())
            minHGB = float(self.minHGB.text())
            maxHGB = float(self.maxHGB.text())
            minMCH = float(self.minMCH.text())
            maxMCH = float(self.maxMCH.text())
            minMCHC = float(self.minMCHC.text())
            maxMCHC = float(self.maxMCHC.text())
            minMPV = float(self.minMPV.text())
            maxMPV = float(self.maxMPV.text())
            minPLT = float(self.minPLT.text())
            maxPLT = float(self.maxPLT.text())
            # check which of the checkboxes are checked
            surv = self.get_excluded_value(self.survY.isChecked(), self.survN.isChecked())
            sex = self.get_excluded_value(self.sexF.isChecked(), self.sexM.isChecked())
            species = self.get_excluded_value(self.speciesPV.isChecked(), self.speciesHG.isChecked())
            minStr = (self.get_year())[0]
            maxStr = (self.get_year())[1]
        except:
            pop_message_box("Something went wrong. The input fields contain non-numeric input, change it.")
            noNumInput = True

        # get the column name for sorting
        orderBy = self.orderBy.currentText()
        if orderBy == 'Default':
            orderBy = 'sealTag'

        # ascending or descending
        sortIn = self.order.currentText()
        if sortIn == 'Ascending':
            isAscending = True
        else:
            isAscending = False

        if not noNumInput:
            connection = sqlite3.connect(DB_PATH)
            c = connection.cursor()
            try:
                sql = """SELECT * FROM sealPredictionData WHERE WBC >= ? and WBC <= ? and LYMF >= ? and LYMF <= ? and 
                GRAN >= ? and GRAN <= ? and MID >= ? and MID <= ? and HCT >= ? and HCT <= ? and MCV >= ? and MCV <= ?
                and RBC >= ? and RBC <= ? and HGB >= ? and HGB <= ? and MCH >= ? and MCH <= ? and MCHC >= ? and MCHC <= ? 
                and MPV >= ? and MPV <= ? and PLT >= ? and PLT <= ? and Survival != ? and Sex != ? and Species != ? and 
                sealTag >= ? and sealTag <= ?"""
                c.execute(sql, (minWBC, maxWBC, minLYMF, maxLYMF, minGRAN, maxGRAN, minMID, maxMID, minHCT, maxHCT, minMCV,
                                maxMCV, minRBC, maxRBC, minHGB, maxHGB, minMCH, maxMCH, minMCHC, maxMCHC, minMPV,
                                maxMPV, minPLT, maxPLT, surv, sex, species, minStr, maxStr))
                sealData = c.fetchall()
                npSealData = np.array(sealData)
                if (npSealData.size != 0):
                    df = pd.DataFrame(npSealData,
                                      columns=['sealTag', 'WBC', 'LYMF', 'GRAN', 'MID', 'HCT', 'MCV', 'RBC', 'HGB',
                                               'MCH', 'MCHC', 'MPV', 'PLT', 'Survival', 'Sex', 'Species'])
                    df = df.astype({'WBC': np.float, 'LYMF': np.float, 'GRAN': np.float, 'MID': np.float,
                                    'HCT': np.float, 'MCV': np.float, 'RBC': np.float, 'HGB': np.float, 'MCH': np.float,
                                    'MCHC': np.float, 'MPV': np.float, 'PLT': np.float})
                    df.sort_values(orderBy, ascending=isAscending, inplace=True)
                    self.update_dataframe(df)
                    self.save_data(df)
                else:
                    pop_message_box("There is no data to save.")
            except:
                pop_message_box("Something went wrong when querying")
            connection.close()

    def update_dataframe(self, df):
        """
        Update sex, species and survival columns of a dataframe
        :param df: the dataframe to be updated
        """
        df['Sex'] = df['Sex'].map({'0': 'Female',
                                   '1': 'Male'},
                                  na_action=None)
        df['Species'] = df['Species'].map({'0': 'Phoca Vitulina',
                                           '1': 'Halichoerus Grypus'},
                                          na_action=None)
        df['Survival'] = df['Survival'].map({'0': 'Not released',
                                             '1': 'Released'},
                                            na_action=None)

    def set_default_values(self):
        """
        Set default values for the blood parameters
        """
        connection = sqlite3.connect(DB_PATH)
        c = connection.cursor()
        # min wbc
        if self.minWBC.text() == "":
            try:
                sql = """SELECT min(WBC) FROM sealPredictionData"""
                c.execute(sql, ())
                minWBC = c.fetchall()
                self.minWBC.setText(str(minWBC[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max wbc
        if self.maxWBC.text() == "":
            try:
                sql = """SELECT max(WBC) FROM sealPredictionData"""
                c.execute(sql, ())
                maxWBC = c.fetchall()
                self.maxWBC.setText(str(maxWBC[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min lymf
        if self.minLYMF.text() == "":
            try:
                sql = """SELECT min(LYMF) FROM sealPredictionData"""
                c.execute(sql, ())
                minLYMF = c.fetchall()
                self.minLYMF.setText(str(minLYMF[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max lymf
        if self.maxLYMF.text() == "":
            try:
                sql = """SELECT max(LYMF) FROM sealPredictionData"""
                c.execute(sql, ())
                maxLYMF = c.fetchall()
                self.maxLYMF.setText(str(maxLYMF[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min gran
        if self.minGRAN.text() == "":
            try:
                sql = """SELECT min(GRAN) FROM sealPredictionData"""
                c.execute(sql, ())
                minGRAN = c.fetchall()
                self.minGRAN.setText(str(minGRAN[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max gran
        if self.maxGRAN.text() == "":
            try:
                sql = """SELECT max(GRAN) FROM sealPredictionData"""
                c.execute(sql, ())
                maxGRAN = c.fetchall()
                self.maxGRAN.setText(str(maxGRAN[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min mid
        if self.minMID.text() == "":
            try:
                sql = """SELECT min(MID) FROM sealPredictionData"""
                c.execute(sql, ())
                minMID = c.fetchall()
                self.minMID.setText(str(minMID[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max mid
        if self.maxMID.text() == "":
            try:
                sql = """SELECT max(MID) FROM sealPredictionData"""
                c.execute(sql, ())
                maxMID = c.fetchall()
                self.maxMID.setText(str(maxMID[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min hct
        if self.minHCT.text() == "":
            try:
                sql = """SELECT min(HCT) FROM sealPredictionData"""
                c.execute(sql, ())
                minHCT = c.fetchall()
                self.minHCT.setText(str(minHCT[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max hct
        if self.maxHCT.text() == "":
            try:
                sql = """SELECT max(HCT) FROM sealPredictionData"""
                c.execute(sql, ())
                maxHCT = c.fetchall()
                self.maxHCT.setText(str(maxHCT[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min mcv
        if self.minMCV.text() == "":
            try:
                sql = """SELECT min(MCV) FROM sealPredictionData"""
                c.execute(sql, ())
                minMCV = c.fetchall()
                self.minMCV.setText(str(minMCV[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max mcv
        if self.maxMCV.text() == "":
            try:
                sql = """SELECT max(MCV) FROM sealPredictionData"""
                c.execute(sql, ())
                maxMCV = c.fetchall()
                self.maxMCV.setText(str(maxMCV[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min rbc
        if self.minRBC.text() == "":
            try:
                sql = """SELECT min(RBC) FROM sealPredictionData"""
                c.execute(sql, ())
                minRBC = c.fetchall()
                self.minRBC.setText(str(minRBC[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max rbc
        if self.maxRBC.text() == "":
            try:
                sql = """SELECT max(RBC) FROM sealPredictionData"""
                c.execute(sql, ())
                maxRBC = c.fetchall()
                self.maxRBC.setText(str(maxRBC[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min hgb
        if self.minHGB.text() == "":
            try:
                sql = """SELECT min(HGB) FROM sealPredictionData"""
                c.execute(sql, ())
                minHGB = c.fetchall()
                self.minHGB.setText(str(minHGB[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max hgb
        if self.maxHGB.text() == "":
            try:
                sql = """SELECT max(HGB) FROM sealPredictionData"""
                c.execute(sql, ())
                maxHGB = c.fetchall()
                self.maxHGB.setText(str(maxHGB[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min mch
        if self.minMCH.text() == "":
            try:
                sql = """SELECT min(MCH) FROM sealPredictionData"""
                c.execute(sql, ())
                minMCH = c.fetchall()
                self.minMCH.setText(str(minMCH[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max mch
        if self.maxMCH.text() == "":
            try:
                sql = """SELECT max(MCH) FROM sealPredictionData"""
                c.execute(sql, ())
                maxMCH = c.fetchall()
                self.maxMCH.setText(str(maxMCH[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min mchc
        if self.minMCHC.text() == "":
            try:
                sql = """SELECT min(MCHC) FROM sealPredictionData"""
                c.execute(sql, ())
                minMCHC = c.fetchall()
                self.minMCHC.setText(str(minMCHC[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max mchc
        if self.maxMCHC.text() == "":
            try:
                sql = """SELECT max(MCHC) FROM sealPredictionData"""
                c.execute(sql, ())
                maxMCHC = c.fetchall()
                self.maxMCHC.setText(str(maxMCHC[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min mpv
        if self.minMPV.text() == "":
            try:
                sql = """SELECT min(MPV) FROM sealPredictionData"""
                c.execute(sql, ())
                minMPV = c.fetchall()
                self.minMPV.setText(str(minMPV[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max mpv
        if self.maxMPV.text() == "":
            try:
                sql = """SELECT max(MPV) FROM sealPredictionData"""
                c.execute(sql, ())
                maxMPV = c.fetchall()
                self.maxMPV.setText(str(maxMPV[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # min plt
        if self.minPLT.text() == "":
            try:
                sql = """SELECT min(PLT) FROM sealPredictionData"""
                c.execute(sql, ())
                minPLT = c.fetchall()
                self.minPLT.setText(str(minPLT[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        # max plt
        if self.maxPLT.text() == "":
            try:
                sql = """SELECT max(PLT) FROM sealPredictionData"""
                c.execute(sql, ())
                maxPLT = c.fetchall()
                self.maxPLT.setText(str(maxPLT[0][0]))
            except:
                pop_message_box("Something went wrong when querying")
        connection.close()

    def set_elements(self):
        """
        Sets the elements of the window
        :return: the layout of the window
        """
        # Setting placeholder tests for blood values:
        self.minWBC.setPlaceholderText("min WBC")
        self.maxWBC.setPlaceholderText("max WBC")
        self.minLYMF.setPlaceholderText("min LYMF")
        self.maxLYMF.setPlaceholderText("max LYMF")
        self.minGRAN.setPlaceholderText("min GRAN")
        self.maxGRAN.setPlaceholderText("max GRAN")
        self.minMID.setPlaceholderText("min MID")
        self.maxMID.setPlaceholderText("max MID")
        self.minHCT.setPlaceholderText("min HCT")
        self.maxHCT.setPlaceholderText("max HCT")
        self.minMCV.setPlaceholderText("min MCV")
        self.maxMCV.setPlaceholderText("max MCV")
        self.minRBC.setPlaceholderText("min RBC")
        self.maxRBC.setPlaceholderText("max RBC")
        self.minHGB.setPlaceholderText("min HGB")
        self.maxHGB.setPlaceholderText("max HGB")
        self.minMCH.setPlaceholderText("min MCH")
        self.maxMCH.setPlaceholderText("max MCH")
        self.minMCHC.setPlaceholderText("min MCHC")
        self.maxMCHC.setPlaceholderText("max MCHC")
        self.minMPV.setPlaceholderText("min MPV")
        self.maxMPV.setPlaceholderText("max MPV")
        self.minPLT.setPlaceholderText("min PLT")
        self.maxPLT.setPlaceholderText("max PLT")

        self.minYear.setPlaceholderText('min Year')
        self.maxYear.setPlaceholderText('max Year')

        # Set placeholder for filename text field
        self.fileName.setPlaceholderText("Enter a file name")

        # Set order by
        self.orderBy.addItem("Default")
        self.orderBy.addItem("WBC")
        self.orderBy.addItem("LYMF")
        self.orderBy.addItem("GRAN")
        self.orderBy.addItem("MID")
        self.orderBy.addItem("HCT")
        self.orderBy.addItem("MCV")
        self.orderBy.addItem("RBC")
        self.orderBy.addItem("HGB")
        self.orderBy.addItem("MCH")
        self.orderBy.addItem("MCHC")
        self.orderBy.addItem("MPV")
        self.orderBy.addItem("PLT")
        self.orderBy.addItem("Year")

        # Set by ascending or descending
        self.order.addItem("Ascending")
        self.order.addItem("Descending")

        self.executeButton.clicked.connect(self.execute_query)
        self.home_button.clicked.connect(self.go_to_home)

        # Add blood values to layout
        # Column 3 is a spacer
        layout = QGridLayout()
        layout.setColumnMinimumWidth(3, 100)
        layout.addWidget(self.infoLabel1, 0, 0, 1, 7)
        layout.setRowMinimumHeight(0, 70)

        layout.addWidget(QLabel('WBC:'), 1, 0)
        layout.addWidget(self.minWBC, 1, 1)
        layout.addWidget(self.maxWBC, 1, 2)
        layout.addWidget(QLabel('LYMF:'), 1, 4)
        layout.addWidget(self.minLYMF, 1, 5)
        layout.addWidget(self.maxLYMF, 1, 6)

        layout.addWidget(QLabel('GRAN:'), 2, 0)
        layout.addWidget(self.minGRAN, 2, 1)
        layout.addWidget(self.maxGRAN, 2, 2)
        layout.addWidget(QLabel('MID:'), 2, 4)
        layout.addWidget(self.minMID, 2, 5)
        layout.addWidget(self.maxMID, 2, 6)

        layout.addWidget(QLabel('HCT:'), 3, 0)
        layout.addWidget(self.minHCT, 3, 1)
        layout.addWidget(self.maxHCT, 3, 2)
        layout.addWidget(QLabel('MCV:'), 3, 4)
        layout.addWidget(self.minMCV, 3, 5)
        layout.addWidget(self.maxMCV, 3, 6)

        layout.addWidget(QLabel('RBC:'), 4, 0)
        layout.addWidget(self.minRBC, 4, 1)
        layout.addWidget(self.maxRBC, 4, 2)
        layout.addWidget(QLabel('HGB:'), 4, 4)
        layout.addWidget(self.minHGB, 4, 5)
        layout.addWidget(self.maxHGB, 4, 6)

        layout.addWidget(QLabel('MCH:'), 5, 0)
        layout.addWidget(self.minMCH, 5, 1)
        layout.addWidget(self.maxMCH, 5, 2)
        layout.addWidget(QLabel('MCHC:'), 5, 4)
        layout.addWidget(self.minMCHC, 5, 5)
        layout.addWidget(self.maxMCHC, 5, 6)

        layout.addWidget(QLabel('MPV:'), 6, 0)
        layout.addWidget(self.minMPV, 6, 1)
        layout.addWidget(self.maxMPV, 6, 2)
        layout.addWidget(QLabel('PLT:'), 6, 4)
        layout.addWidget(self.minPLT, 6, 5)
        layout.addWidget(self.maxPLT, 6, 6)

        # Add year to layout
        layout.addWidget(QLabel('Year:'), 7, 0)
        layout.addWidget(self.minYear, 7, 1)
        layout.addWidget(self.maxYear, 7, 2)

        layout.addWidget(self.infoLabel2, 8, 0, 1, 7)
        layout.setRowMinimumHeight(8, 70)

        # Add survival to layout
        layout.addWidget(QLabel('Survival:'), 9, 0)
        layout.addWidget(self.survY, 9, 1)
        layout.addWidget(self.survN, 9, 2)
        # Add sex to layout
        layout.addWidget(QLabel('Sex:'), 9, 4)
        layout.addWidget(self.sexF, 9, 5)
        layout.addWidget(self.sexM, 9, 6)

        # Add species to layout
        layout.addWidget(QLabel('Species:'), 10, 0)
        layout.addWidget(self.speciesPV, 10, 1)
        layout.addWidget(self.speciesHG, 10, 2)
        # Add order by to layout
        layout.addWidget(QLabel('Sort by:'), 10, 4)
        layout.addWidget(self.orderBy, 10, 5)
        # Add order by ascending or descending
        layout.addWidget(self.order, 10, 6)

        layout.setRowMinimumHeight(11, 50)
        layout.addWidget(self.infoLabel3, 12, 0, 1, 7)
        # Add text field for filename
        layout.addWidget(self.fileName, 13, 0, 1, 3)
        layout.addWidget(self.executeButton, 13, 3, 1, 2)

        layout.addWidget(self.home_button, 13, 6)
        # layout.setRowMinimumHeight(14, 80)

        layout.setRowStretch(25, 1)
        # layout.setColumnMinimumWidth(0, 150)

        return layout
