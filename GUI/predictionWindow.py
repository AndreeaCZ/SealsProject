from pathlib import Path

import joblib
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import *
from openpyxl import load_workbook
from openpyxl.workbook import Workbook

from GUI.utils import *
from variables import MODEL_PATH, DIV

########################################################################################################################
# Represents the window where the user can predict the outcome of a seal
########################################################################################################################

defaultFeatureList = ["WBC", "LYMF", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]
defaultModelName = "Default"


class PredictionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.sealData = None
        self.modelName = defaultModelName
        self.featureList = defaultFeatureList
        self.model = joblib.load(MODEL_PATH)
        self.setWindowTitle("Run predictions")
        self.setFixedSize(QSize(700, 400))
        self.layout = QGridLayout()

        # Creating elements:
        self.input_filename = QLineEdit()
        self.import_button = QPushButton('Import')
        self.output_label = QLabel()
        self.save_button = QPushButton('Save')
        self.image_label = QLabel()
        self.load_model_button = QPushButton('Load a model')
        self.load_default_model_button = QPushButton('Default model')
        # Creating import sub fields
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()

        # Set widget properties:
        self.set_elements()
        self.setAutoFillBackground(True)
        self.setLayout(self.layout)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)

    def set_elements(self):
        """
        Sets the elements of the window
        :return: the layout of the window
        """
        # Setting elements properties:
        self.combo1.addItem("Female")
        self.combo1.addItem("Male")
        self.combo2.addItem("Phoca Vitulina")
        self.combo2.addItem("Halichoerus Grypus")
        self.input_filename.setPlaceholderText('Enter an excel file name')
        self.import_button.clicked.connect(self.get_import)
        self.output_label.setText('Enter data to see prediction')
        self.load_model_button.clicked.connect(self.load_model)
        self.load_default_model_button.clicked.connect(self.load_default_model)
        self.save_button.clicked.connect(self.save_results)
        # Adding elements to input layout:
        self.layout.addWidget(self.combo1, 1, 0, 1, 2)
        self.layout.addWidget(self.combo2, 2, 0, 1, 2)
        self.layout.addWidget(self.import_button, 4, 2)
        self.layout.addWidget(self.load_default_model_button, 1, 2)
        self.layout.addWidget(self.load_model_button, 2, 2)
        self.layout.addWidget(self.output_label, 4, 0, 1, 2)
        self.layout.addWidget(self.save_button, 5, 2)
        self.layout.addWidget(self.input_filename, 5, 0)
        self.layout.setRowStretch(5, 1)
        self.layout.setRowMinimumHeight(3, 100)
        self.layout.setRowMinimumHeight(4, 100)

    # loads the default model with a different message
    def load_default_model_with_new_msg(self):
        self.output_label.setText("")
        self.modelName = defaultModelName
        self.model = joblib.load(MODEL_PATH)
        self.featureList = defaultFeatureList
        pop_message_box("Can't find the featuresChecklist.xlsx file. Default model loaded successfully")

    # Update the list of features used for predicting based on the parameters the new model was trained on
    def update_feature_list(self, filename):
        try:
            wb = load_workbook("featuresChecklist.xlsx")
            ws = wb.active
            maxCol = ws.max_column
            maxRow = ws.max_row
            featureListTemp = []
            flag = False
            colNum = -1
            # find the column corresponding to the loaded model
            for j in range(2, maxCol + 1):
                if ws.cell(row=1, column=j).value == filename:
                    flag = True
                    colNum = j
                    break
            # The model file exists but its data is not present in the features checklist
            if not flag:
                pop_message_box("Please select another model")
            else:
                # create a list of features the model was trained on
                self.modelName = ws.cell(row=1, column=colNum).value
                for i in range(2, maxRow + 1):
                    if ws.cell(row=i, column=colNum).value is not None:
                        featureListTemp.append(ws.cell(row=i, column=1).value)
                self.featureList = featureListTemp
                pop_message_box("Model loaded successfully")
        except:
            self.load_default_model_with_new_msg()

    # saves the results of the prediction
    def save_results(self):
        self.output_label.setText("")
        fileName = self.input_filename.text()
        if fileName == "":
            pop_message_box("Please enter a file name first.")
        else:
            # the user tries to save a model only after training it
            if not (self.sealData is None or self.sealData == []):
                import_path = QFileDialog.getExistingDirectoryUrl().path()
                if not (import_path == ""):
                    import_path = import_path + DIV + fileName + '.xlsx'
                    self.save_prediction(import_path)
                    # pops a message box
                    pop_message_box("Prediction saved successfully")
                    self.sealData = None
            else:
                pop_message_box("Please predict something first.")
            self.input_filename.setText("")
        self.sealData = None

    def save_prediction(self, import_path):
        # Create an Excel file
        excelFile = Workbook()
        spreadSheet = excelFile.active

        featureListLength = len(self.featureList)
        sealDataLength = len(self.sealData)

        # Fill in the features
        spreadSheet.cell(row=1, column=1).value = "MODEL NAME"
        for i in range(featureListLength):
            spreadSheet.cell(row=i + 2, column=1).value = self.featureList[i]
        spreadSheet.cell(row=featureListLength + 2, column=1).value = "SEX"
        spreadSheet.cell(row=featureListLength + 3, column=1).value = "SPECIES"
        spreadSheet.cell(row=featureListLength + 4, column=1).value = "SURVIVAL"

        # Fill in the values
        spreadSheet.cell(row=1, column=2).value = self.modelName
        for i in range(len(self.sealData) - 3):
            spreadSheet.cell(row=i + 2, column=2).value = self.sealData[i]

        spreadSheet.cell(row=sealDataLength - 1, column=2).value = get_sex_str_from_int(self.sealData[sealDataLength - 3])
        spreadSheet.cell(row=sealDataLength, column=2).value = get_seal_species_str_from_int(
            self.sealData[sealDataLength - 2])
        spreadSheet.cell(row=sealDataLength + 1, column=2).value = get_chances_str_from_int(
            self.sealData[sealDataLength - 1])

        excelFile.save(import_path)

    # Load the default model
    def load_default_model(self):
        self.output_label.setText("")
        self.modelName = defaultModelName
        self.model = joblib.load(MODEL_PATH)
        self.featureList = defaultFeatureList
        pop_message_box("Default model loaded successfully")

    # Load a model from the local machine
    def load_model(self):
        self.output_label.setText("")
        import_path = QFileDialog.getOpenFileName(filter='PKL files (*.pkl)')[0]
        if not (import_path == ""):
            self.model = joblib.load(import_path)
            fileName = Path(import_path).stem
            self.update_feature_list(fileName)

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
        sex1 = get_sex_int(sex)
        species1 = get_seal_species_int(species)
        if not import_path_null:
            result, self.sealData = make_prediction(import_path, sex1, species1, self.model, self.featureList)
        if not (result == 0):
            self.output_label.setText(result)
