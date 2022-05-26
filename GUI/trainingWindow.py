from sqlite3 import connect
import joblib
import numpy as np
import pandas as pd
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import xlsxwriter
from variables import DB_PATH, DIV
from openpyxl import load_workbook

# Represents the window that lets the user train their own model
class TrainModelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.MODEL = None
        self.excelRowIndex = [2,3,4,5,6,7,8,9]
        self.setFixedSize(QSize(500, 300))
        self.setWindowTitle("Train a model")
        self.wbc = QCheckBox("WBC")
        self.lymf = QCheckBox("LYMF")
        self.rbc = QCheckBox("RBC")
        self.hgb = QCheckBox("HGB")
        self.mch = QCheckBox("MCH")
        self.mchc = QCheckBox("MCHC")
        self.mpv = QCheckBox("MPV")
        self.plt = QCheckBox("PLT")
        layout = QVBoxLayout()
        layout.addWidget(self.wbc)
        layout.addWidget(self.lymf)
        layout.addWidget(self.rbc)
        layout.addWidget(self.hgb)
        layout.addWidget(self.mch)
        layout.addWidget(self.mchc)
        layout.addWidget(self.mpv)
        layout.addWidget(self.plt)
        self.accu_label = QLabel()
        self.accu_label.setText("Model accuracy")
        layout.addWidget(self.accu_label)
        self.train_button = QPushButton('Train')
        self.input_model_name = QLineEdit()
        self.save_button = QPushButton('Save')
        self.train_button.clicked.connect(self.train_new_model)
        self.save_button.clicked.connect(self.save_model)
        layout.addWidget(self.train_button)
        layout.addWidget(self.input_model_name)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    # This function is used to update the Excel file. This Excel file is used to note down all the selected features
    # for the trained models. If a feature was used, then the corresponding cell will be filled with 1.
    def saveFeatures(self, rowIndexList, modelName):
        #load a workbook and worksheet.
        wb = load_workbook("featuresChecklist.xlsx")
        ws = wb.active
        colIndex = 2
        maxCol= ws.max_column
        maxRow = ws.max_row
        # Find the empty column
        for j in range(2, maxCol+1):
            counter = 0
            for i in range(2,maxRow+1):
                if(ws.cell(row=i, column=j).value is None):
                    counter = counter+1
            if counter == maxRow-1:
                break
            else:
                colIndex = colIndex+1
        #Check if a new column is needed
        if colIndex == maxCol:
            ws.insert_cols(maxCol+1)
        #Fill in the corresponding values
        ws.cell(row=1, column=colIndex).value = modelName
        for i in rowIndexList:
            #fill in the cell with 1
            ws.cell(row=i, column=colIndex).value = 1
        wb.save("featuresChecklist.xlsx")

    # pops open a message box with the passed str as the message
    def popMessageBox(self, str):
        msgBox = QMessageBox()
        msgBox.setText(str)
        msgBox.exec()

    # Saves a user trained model
    def save_model(self):
        model_name = self.input_model_name.text()
        self.input_model_name.setText("")
        # model name was given
        if not (model_name == ""):
            import_path = QFileDialog.getExistingDirectoryUrl().path()
            import_path = import_path + DIV + model_name + '.pkl'
            # the user tries to save a model only after training it
            if not (self.model == None):
                #save the model details into the excel file (featuresChecklist.xlsx)
                self.saveFeatures(self.excelRowIndex, model_name)
                joblib.dump(self.model, import_path)
                # pops a message box
                self.popMessageBox("Model saved successfully")
                self.model = None

    # Trains a model based on the features selected
    def train_new_model(self):
        conn = connect(DB_PATH)  # create
        # database connection
        datasetLabeledSeals = pd.read_sql('SELECT *  FROM sealPredictionData', conn)  # import data into dataframe
        datasetLabeledSeals = datasetLabeledSeals.drop(['sealTag', 'HCT', 'MCV'], axis=1)  # drop tag column

        # if a feature is unchecked, it is removed from the training model params
        if not self.wbc.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['WBC'], axis=1)  # drop tag column
            self.excelRowIndex.remove(2)
        if not self.lymf.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['LYMF'], axis=1)  # drop tag column
            self.excelRowIndex.remove(3)
        if not self.rbc.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['RBC'], axis=1)  # drop tag column
            self.excelRowIndex.remove(4)
        if not self.hgb.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['HGB'], axis=1)  # drop tag column
            self.excelRowIndex.remove(5)
        if not self.mch.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['MCH'], axis=1)  # drop tag column
            self.excelRowIndex.remove(6)
        if not self.mchc.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['MCHC'], axis=1)  # drop tag column
            self.excelRowIndex.remove(7)
        if not self.mpv.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['MPV'], axis=1)  # drop tag column
            self.excelRowIndex.remove(8)
        if not self.plt.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['PLT'], axis=1)  # drop tag column
            self.excelRowIndex.remove(9)

        #save features in an excel file
        #self.saveFeatures(self.excelRowIndex)

        # print(datasetLabeledSeals['Survival'].value_counts())  # check unbalanced data
        survivalDecisionTree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_leaf=6)
        X = datasetLabeledSeals.drop(['Survival'], axis=1)  # separate features from labels
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)  # normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
        y = datasetLabeledSeals['Survival'].values  # get all labels

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                            random_state=42)  # split data into training
        # and test
        self.model = survivalDecisionTree.fit(X_train, y_train)  # train the model
        predictions = survivalDecisionTree.predict(X_test)  # make predictions on the test set
        self.accu_label.setText("Your new model's accuracy " + str(accuracy_score(y_test, predictions)) + "%")
        self.popMessageBox("Model trained successfully")

