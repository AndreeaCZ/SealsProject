import sqlite3

import numpy as np
import pandas as pd
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QCheckBox, QComboBox, QGridLayout, QFileDialog, QLabel
import datetime

from GUI.utils import lightgray, pop_message_box
from variables import DB_PATH, DIV


query_error = "Something went wrong when querying"

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
            min_year = 2014
        else:
            min_year = int(float(self.minYear.text()))

        if (self.maxYear.text() == ""):
            current_date_time = datetime.datetime.now()
            date = current_date_time.date()
            max_year = int(date.strftime("%Y"))
        else:
            max_year = int(float(self.maxYear.text()))

        min_str = self.get_min_tag_for_year(min_year)
        max_str = self.get_max_tag_for_year(max_year)
        return min_str, max_str

    def save_data(self, df):
        """
        Saves the data from the dataframe passed into an excel file
        :param df: the dataframe to be saved
        """
        file_name = self.fileName.text()
        if file_name == "":
            pop_message_box("Please enter a file name first.")
        else:
            import_path = QFileDialog.getExistingDirectoryUrl().path()
            if import_path != "":
                import_path = import_path + DIV + file_name + '.xlsx'
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
        no_num_input = False
        try:
            min_wbc = float(self.minWBC.text())
            max_wbc = float(self.maxWBC.text())
            min_lymf = float(self.minLYMF.text())
            max_lymf = float(self.maxLYMF.text())
            min_gran = float(self.minGRAN.text())
            max_gran = float(self.maxGRAN.text())
            min_mid = float(self.minMID.text())
            max_mid = float(self.maxMID.text())
            min_hct = float(self.minHCT.text())
            max_hct = float(self.maxHCT.text())
            min_mcv = float(self.minMCV.text())
            max_mcv = float(self.maxMCV.text())
            min_rbc = float(self.minRBC.text())
            max_rbc = float(self.maxRBC.text())
            min_hgb = float(self.minHGB.text())
            max_hgb = float(self.maxHGB.text())
            min_mch = float(self.minMCH.text())
            max_mch = float(self.maxMCH.text())
            min_mchc = float(self.minMCHC.text())
            max_mchc = float(self.maxMCHC.text())
            min_mpv = float(self.minMPV.text())
            max_mpv = float(self.maxMPV.text())
            min_plt = float(self.minPLT.text())
            max_plt = float(self.maxPLT.text())
            # check which of the checkboxes are checked
            surv = self.get_excluded_value(self.survY.isChecked(), self.survN.isChecked())
            sex = self.get_excluded_value(self.sexF.isChecked(), self.sexM.isChecked())
            species = self.get_excluded_value(self.speciesPV.isChecked(), self.speciesHG.isChecked())
            min_str = (self.get_year())[0]
            max_str = (self.get_year())[1]
        except ValueError:
            pop_message_box("Something went wrong. The input fields contain non-numeric input, change it.")
            no_num_input = True

        # get the column name for sorting
        order_by = self.orderBy.currentText()
        if order_by == 'Default':
            order_by = 'sealTag'

        # ascending or descending
        sort_in = self.order.currentText()
        if sort_in == 'Ascending':
            is_ascending = True
        else:
            is_ascending = False

        if not no_num_input:
            connection = sqlite3.connect(DB_PATH)
            c = connection.cursor()
            try:
                sql = """SELECT * FROM sealPredictionData WHERE WBC >= ? and WBC <= ? and LYMF >= ? and LYMF <= ? and 
                GRAN >= ? and GRAN <= ? and MID >= ? and MID <= ? and HCT >= ? and HCT <= ? and MCV >= ? and MCV <= ?
                and RBC >= ? and RBC <= ? and HGB >= ? and HGB <= ? and MCH >= ? and MCH <= ? and MCHC >= ? and MCHC <= ? 
                and MPV >= ? and MPV <= ? and PLT >= ? and PLT <= ? and Survival != ? and Sex != ? and Species != ? and 
                sealTag >= ? and sealTag <= ?"""
                c.execute(sql, (min_wbc, max_wbc, min_lymf, max_lymf, min_gran, max_gran, min_mid, max_mid, min_hct, max_hct, min_mcv,
                                max_mcv, min_rbc, max_rbc, min_hgb, max_hgb, min_mch, max_mch, min_mchc, max_mchc, min_mpv,
                                max_mpv, min_plt, max_plt, surv, sex, species, min_str, max_str))
                seal_data = c.fetchall()
                np_seal_data = np.array(seal_data)
                if (np_seal_data.size != 0):
                    df = pd.DataFrame(np_seal_data,
                                      columns=['sealTag', 'WBC', 'LYMF', 'GRAN', 'MID', 'HCT', 'MCV', 'RBC', 'HGB',
                                               'MCH', 'MCHC', 'MPV', 'PLT', 'Survival', 'Sex', 'Species'])
                    df = df.astype({'WBC': np.float, 'LYMF': np.float, 'GRAN': np.float, 'MID': np.float,
                                    'HCT': np.float, 'MCV': np.float, 'RBC': np.float, 'HGB': np.float, 'MCH': np.float,
                                    'MCHC': np.float, 'MPV': np.float, 'PLT': np.float})
                    df.sort_values(order_by, ascending=is_ascending, inplace=True)
                    self.update_dataframe(df)
                    self.save_data(df)
                else:
                    pop_message_box("There is no data to save.")
            except sqlite3.OperationalError:
                pop_message_box(query_error)
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
                min_wbc = c.fetchall()
                self.minWBC.setText(str(min_wbc[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max wbc
        if self.maxWBC.text() == "":
            try:
                sql = """SELECT max(WBC) FROM sealPredictionData"""
                c.execute(sql, ())
                max_wbc = c.fetchall()
                self.maxWBC.setText(str(max_wbc[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min lymf
        if self.minLYMF.text() == "":
            try:
                sql = """SELECT min(LYMF) FROM sealPredictionData"""
                c.execute(sql, ())
                min_lymf = c.fetchall()
                self.minLYMF.setText(str(min_lymf[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max lymf
        if self.maxLYMF.text() == "":
            try:
                sql = """SELECT max(LYMF) FROM sealPredictionData"""
                c.execute(sql, ())
                max_lymf = c.fetchall()
                self.maxLYMF.setText(str(max_lymf[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min gran
        if self.minGRAN.text() == "":
            try:
                sql = """SELECT min(GRAN) FROM sealPredictionData"""
                c.execute(sql, ())
                min_gran = c.fetchall()
                self.minGRAN.setText(str(min_gran[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max gran
        if self.maxGRAN.text() == "":
            try:
                sql = """SELECT max(GRAN) FROM sealPredictionData"""
                c.execute(sql, ())
                max_gran = c.fetchall()
                self.maxGRAN.setText(str(max_gran[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min mid
        if self.minMID.text() == "":
            try:
                sql = """SELECT min(MID) FROM sealPredictionData"""
                c.execute(sql, ())
                min_mid = c.fetchall()
                self.minMID.setText(str(min_mid[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max mid
        if self.maxMID.text() == "":
            try:
                sql = """SELECT max(MID) FROM sealPredictionData"""
                c.execute(sql, ())
                max_mid = c.fetchall()
                self.maxMID.setText(str(max_mid[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min hct
        if self.minHCT.text() == "":
            try:
                sql = """SELECT min(HCT) FROM sealPredictionData"""
                c.execute(sql, ())
                min_hct = c.fetchall()
                self.minHCT.setText(str(min_hct[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max hct
        if self.maxHCT.text() == "":
            try:
                sql = """SELECT max(HCT) FROM sealPredictionData"""
                c.execute(sql, ())
                max_hct = c.fetchall()
                self.maxHCT.setText(str(max_hct[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min mcv
        if self.minMCV.text() == "":
            try:
                sql = """SELECT min(MCV) FROM sealPredictionData"""
                c.execute(sql, ())
                min_mcv = c.fetchall()
                self.minMCV.setText(str(min_mcv[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max mcv
        if self.maxMCV.text() == "":
            try:
                sql = """SELECT max(MCV) FROM sealPredictionData"""
                c.execute(sql, ())
                max_mcv = c.fetchall()
                self.maxMCV.setText(str(max_mcv[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min rbc
        if self.minRBC.text() == "":
            try:
                sql = """SELECT min(RBC) FROM sealPredictionData"""
                c.execute(sql, ())
                min_rbc = c.fetchall()
                self.minRBC.setText(str(min_rbc[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max rbc
        if self.maxRBC.text() == "":
            try:
                sql = """SELECT max(RBC) FROM sealPredictionData"""
                c.execute(sql, ())
                max_rbc = c.fetchall()
                self.maxRBC.setText(str(max_rbc[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min hgb
        if self.minHGB.text() == "":
            try:
                sql = """SELECT min(HGB) FROM sealPredictionData"""
                c.execute(sql, ())
                min_hgb = c.fetchall()
                self.minHGB.setText(str(min_hgb[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max hgb
        if self.maxHGB.text() == "":
            try:
                sql = """SELECT max(HGB) FROM sealPredictionData"""
                c.execute(sql, ())
                max_hgb = c.fetchall()
                self.maxHGB.setText(str(max_hgb[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min mch
        if self.minMCH.text() == "":
            try:
                sql = """SELECT min(MCH) FROM sealPredictionData"""
                c.execute(sql, ())
                min_mch = c.fetchall()
                self.minMCH.setText(str(min_mch[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max mch
        if self.maxMCH.text() == "":
            try:
                sql = """SELECT max(MCH) FROM sealPredictionData"""
                c.execute(sql, ())
                max_mch = c.fetchall()
                self.maxMCH.setText(str(max_mch[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min mchc
        if self.minMCHC.text() == "":
            try:
                sql = """SELECT min(MCHC) FROM sealPredictionData"""
                c.execute(sql, ())
                min_mchc = c.fetchall()
                self.minMCHC.setText(str(min_mchc[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max mchc
        if self.maxMCHC.text() == "":
            try:
                sql = """SELECT max(MCHC) FROM sealPredictionData"""
                c.execute(sql, ())
                max_mchc = c.fetchall()
                self.maxMCHC.setText(str(max_mchc[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min mpv
        if self.minMPV.text() == "":
            try:
                sql = """SELECT min(MPV) FROM sealPredictionData"""
                c.execute(sql, ())
                min_mpv = c.fetchall()
                self.minMPV.setText(str(min_mpv[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max mpv
        if self.maxMPV.text() == "":
            try:
                sql = """SELECT max(MPV) FROM sealPredictionData"""
                c.execute(sql, ())
                max_mpv = c.fetchall()
                self.maxMPV.setText(str(max_mpv[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # min plt
        if self.minPLT.text() == "":
            try:
                sql = """SELECT min(PLT) FROM sealPredictionData"""
                c.execute(sql, ())
                min_plt = c.fetchall()
                self.minPLT.setText(str(min_plt[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
        # max plt
        if self.maxPLT.text() == "":
            try:
                sql = """SELECT max(PLT) FROM sealPredictionData"""
                c.execute(sql, ())
                max_plt = c.fetchall()
                self.maxPLT.setText(str(max_plt[0][0]))
            except SyntaxError:
                pop_message_box(query_error)
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
