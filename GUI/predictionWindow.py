from pathlib import Path

import joblib
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import *
from openpyxl import load_workbook

from GUI.utils import *
from variables import MODEL_PATH

defaultFeatureList = ["WBC", "LYMF", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]

class PredictionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.result = 0
        self.featureList = defaultFeatureList
        self.model = joblib.load(MODEL_PATH)
        self.setWindowTitle("Run predictions")
        self.setFixedSize(QSize(700, 400))
        self.layout = QGridLayout()

        # Creating elements:
        self.input_line = QLineEdit()
        self.import_button = QPushButton('Import')
        self.output_label = QLabel()
        self.save_button = QPushButton('Save')
        self.image_label = QLabel()
        self.load_model_button = QPushButton('Load a model')
        self.load_default_model_button = QPushButton('Default model')
        # Creating import sub fields
        self.combo1 = QComboBox()
        self.combo1.addItem("Female")
        self.combo1.addItem("Male")
        self.combo2 = QComboBox()
        self.combo2.addItem("Phoca Vitulina")
        self.combo2.addItem("Halichoerus Grypus")

        # Set widget properties:
        self.setAutoFillBackground(True)
        self.set_elements()
        self.setLayout(self.layout)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)

    def set_elements(self):
        # Setting elements properties:
        self.input_line.setFixedWidth(300)
        self.input_line.setPlaceholderText('File Path')
        self.import_button.clicked.connect(self.get_import)
        self.output_label.setText('Enter data to see prediction')
        self.load_model_button.clicked.connect(self.load_model)
        self.load_default_model_button.clicked.connect(self.load_default_model)
        self.save_button.clicked.connect(self.save_results)
        # Adding elements to input layout:
        self.layout.addWidget(self.combo1, 1, 0, 1, 2)
        self.layout.addWidget(self.combo2, 2, 0, 1, 2)
        self.layout.addWidget(self.import_button, 3, 2)
        self.layout.addWidget(self.load_default_model_button, 1,2)
        self.layout.addWidget(self.load_model_button, 2, 2)
        self.layout.addWidget(self.output_label, 4, 0, 1, 2)
        self.layout.addWidget(self.save_button, 4, 2)
        self.layout.setRowStretch(5, 1)
        self.layout.setRowMinimumHeight(3, 100)
        self.layout.setRowMinimumHeight(4, 100)

    # pops open a message box with the passed str as the message
    def popMessageBox(self, str):
        msgBox = QMessageBox()
        msgBox.setText(str)
        msgBox.exec()

    # Update the list of features used for predicting based on the parameters the new model was trained on
    def updateFeatureList(self, filename):
        wb = load_workbook("featuresChecklist.xlsx")
        ws = wb.active
        maxCol = ws.max_column
        maxRow = ws.max_row
        featureListTemp = []
        flag = False
        # find the column corresponding to the loaded model
        for j in range(2, maxCol + 1):
            if (ws.cell(row=1, column=j).value == filename):
                flag = True
                colNum = j
                break
        # The model file exists but its data is not present in the features checklist
        if not flag:
            self.popMessageBox("Please select another model")
        else:
            # create a list of features the model was trained on
            for i in range(2, maxRow+1):
                if (ws.cell(row=i, column=colNum).value is not None):
                    featureListTemp.append(ws.cell(row=i, column=1).value)
            self.featureList = featureListTemp
            self.popMessageBox("Model loaded successfully")

    def save_results(self):
        print(self.result)

    # Load the default model
    def load_default_model(self):
        self.model = joblib.load(MODEL_PATH)
        self.featureList = defaultFeatureList
        self.popMessageBox("Default model loaded successfully")

    # Load a model from the local machine
    def load_model(self):
        import_path = QFileDialog.getOpenFileName(filter='PKL files (*.pkl)')[0]
        if not (import_path == ""):
            self.model = joblib.load(import_path)
            fileName = Path(import_path).stem
            self.updateFeatureList(fileName)

    # if the result is zero, there´s a problem when taking the input
    def get_import(self):
        result = 0
        import_path_null = False
        import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
        # if you open the window file explorer and click cancel
        if import_path == "":
            import_path_null = True
        sex = self.combo1.currentText()
        species = self.combo2.currentText()
        sex1 = getSexInt(sex)
        species1 = getSealSpeciesInt(species)
        if not import_path_null:
            result = make_prediction(import_path, sex1, species1, self.model, self.featureList)
        if not (result == 0):
             self.output_label.setText(result)

def getSealSpeciesInt(str):
        if str == "Phoca Vitulina":
            return 0
        if str == "Halichoerus Grypus":
            return 1

def getSexInt(str):
        if str == "Female":
            return 0
        if str == "Male":
            return 1