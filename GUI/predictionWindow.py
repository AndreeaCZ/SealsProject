from pathlib import Path

import joblib
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import *
from openpyxl import load_workbook
from openpyxl.workbook import Workbook

from GUI.utils import *
from variables import MODEL_PATH, DIV

########################################################################################################################
# Represents the window where the user can predict the outcome of a seal
########################################################################################################################

defaultFeatureList = ["WBC", "LYMF", "GRAN", "MID", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]
defaultModelName = "defaultModel"


class PredictionWindow(QWidget):
    def __init__(self, dashboard):
        super().__init__()
        self.sealData = None
        self.modelName = defaultModelName
        self.featureList = defaultFeatureList
        self.model = joblib.load(MODEL_PATH)
        self.setWindowTitle("Run predictions")
        self.setFixedSize(QSize(600, 750))
        self.dashboard = dashboard
        dashboard.close()

        # Creating elements:
        self.input_filename = QLineEdit()
        self.import_button = QPushButton('Import')
        self.output_label = QLabel('Enter data to see prediction')
        self.save_button = QPushButton('Save')
        self.load_model_button = QPushButton('Load a model')
        self.load_default_model_button = QPushButton('Default model')
        self.info_label_1 = QLabel('Select sex and species')
        self.info_label_2 = QLabel('Select what model to use')
        self.info_label_3 = QLabel('Enter blood test values')
        self.info_label_4 = QLabel('Click to run prediction once all values are entered')
        self.info_label_5 = QLabel('Click to import values from an excel file')
        self.run_predict_button = QPushButton('Predict')

        # Creating import subfields
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.wbc_label = QLabel("WBC: ")
        self.lymf_label = QLabel("LYMF: ")
        self.gran_label = QLabel("GRAN: ")
        self.mid_label = QLabel("MID: ")
        self.rbc_label = QLabel("RBC: ")
        self.hgb_label = QLabel("HGB: ")
        self.mch_label = QLabel("MCH: ")
        self.mchc_label = QLabel("MCHC: ")
        self.mpv_label = QLabel("MPV: ")
        self.plt_label = QLabel("PLT: ")
        self.wbc_input = QLineEdit()
        self.lymf_input = QLineEdit()
        self.gran_input = QLineEdit()
        self.mid_input = QLineEdit()
        self.rbc_input = QLineEdit()
        self.hgb_input = QLineEdit()
        self.mch_input = QLineEdit()
        self.mchc_input = QLineEdit()
        self.mpv_input = QLineEdit()
        self.plt_input = QLineEdit()

        # textField dict
        defaultInputList = [self.wbc_input, self.lymf_input, self.gran_input, self.mid_input, self.rbc_input,
                            self.hgb_input, self.mch_input, self.mchc_input, self.mpv_input, self.plt_input]
        self.featureInputDict = dict(zip(defaultFeatureList, defaultInputList))
        # textField labels dict
        defaultLabelList = [self.wbc_label, self.lymf_label, self.gran_label, self.mid_label, self.rbc_label,
                            self.hgb_label, self.mch_label, self.mchc_label, self.mpv_label, self.plt_label]
        self.featureLabelDict = dict(zip(defaultFeatureList, defaultLabelList))


        # Creating a home button
        self.home_button = QPushButton('Home')

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
        self.load_model_button.clicked.connect(self.load_model)
        self.load_default_model_button.clicked.connect(self.load_default_model)
        self.save_button.clicked.connect(self.save_results)
        self.home_button.clicked.connect(self.go_to_home)
        self.info_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.run_predict_button.clicked.connect(self.run_prediction)
        self.output_label.setAutoFillBackground(True)
        p = self.output_label.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        self.output_label.setPalette(p)
        # Adding elements to input layout:
        layout = QGridLayout()
        layout.addWidget(self.info_label_1, 0, 0, 1, 2)
        layout.addWidget(self.info_label_2, 0, 3)
        layout.addWidget(self.combo1, 1, 0, 1, 2)
        layout.addWidget(self.load_default_model_button, 1, 3)
        layout.addWidget(self.combo2, 2, 0, 1, 2)
        layout.addWidget(self.load_model_button, 2, 3)
        layout.setRowMinimumHeight(3, 50)  # Row 3 is empty and is used as a space
        layout.addWidget(self.info_label_3, 4, 0, 1, 4)

        layout.addWidget(self.wbc_label, 5, 0)
        layout.addWidget(self.lymf_label, 5, 1)
        layout.addWidget(self.gran_label, 5, 2)
        layout.addWidget(self.mid_label, 5, 3)
        layout.addWidget(self.wbc_input, 6, 0)
        layout.addWidget(self.lymf_input, 6, 1)
        layout.addWidget(self.gran_input, 6, 2)
        layout.addWidget(self.mid_input, 6, 3)

        layout.addWidget(self.rbc_label, 7, 0)
        layout.addWidget(self.hgb_label, 7, 1)
        layout.addWidget(self.mch_label, 7, 2)
        layout.addWidget(self.mchc_label, 7, 3)
        layout.addWidget(self.rbc_input, 8, 0)
        layout.addWidget(self.hgb_input, 8, 1)
        layout.addWidget(self.mch_input, 8, 2)
        layout.addWidget(self.mchc_input, 8, 3)

        layout.addWidget(self.mpv_label, 9, 0)
        layout.addWidget(self.plt_label, 9, 1)
        layout.addWidget(self.mpv_input, 10, 0)
        layout.addWidget(self.plt_input, 10, 1)

        layout.addWidget(self.info_label_4, 11, 0, 1, 3)
        layout.addWidget(self.run_predict_button, 11, 3)
        layout.setRowMinimumHeight(12, 50)  # Row 10 is empty and is used as a space
        layout.addWidget(self.info_label_5, 13, 0, 1, 3)
        layout.addWidget(self.import_button, 13, 3)
        layout.addWidget(self.output_label, 14, 0, 1, 4)
        layout.setRowMinimumHeight(14, 100)
        layout.addWidget(self.input_filename, 15, 0, 1, 3)
        layout.addWidget(self.save_button, 15, 3)
        layout.addWidget(self.home_button, 16, 2)
        layout.setRowStretch(16, 1)
        return layout

    # dynamically add input lines and labels
    def update_input_and_labels(self):
        '''
        update the input fields and labels based on the loaded model
        '''
        # hide all labels
        for label in self.featureLabelDict.values():
            label.hide()
        # hide all input fields
        for input in self.featureInputDict.values():
            input.hide()
        # show labels and fields of features in the current feature list
        for feature in self.featureList:
            self.featureLabelDict.get(feature).show()
            self.featureInputDict.get(feature).show()

    # clears the text of all input fields
    def reset_input_fields_text(self):
        for input in self.featureInputDict.values():
            input.setText("")

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
        fileName = self.input_filename.text()
        if fileName == "":
            pop_message_box("Please enter a file name first.")
        else:
            if not (self.sealData is None or self.sealData.size == 0):
                import_path = QFileDialog.getExistingDirectoryUrl().path()
                if not (import_path == ""):
                    import_path = import_path + DIV + fileName + '.xlsx'
                    self.save_prediction(import_path)
                    # pops a message box
                    pop_message_box("Prediction saved successfully")
                    self.sealData = None
                    self.output_label.setText("")
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
        spreadSheet.cell(row=1, column=1).value = "SEAL-TAG"
        spreadSheet.cell(row=2, column=1).value = "MODEL NAME"
        for i in range(featureListLength):
            spreadSheet.cell(row=i + 3, column=1).value = self.featureList[i]
        spreadSheet.cell(row=featureListLength + 3, column=1).value = "SEX"
        spreadSheet.cell(row=featureListLength + 4, column=1).value = "SPECIES"
        spreadSheet.cell(row=featureListLength + 5, column=1).value = "SURVIVAL"

        # Fill in the values
        spreadSheet.cell(row=1, column=2).value = self.sealData[0]
        spreadSheet.cell(row=2, column=2).value = self.modelName
        for i in range(len(self.sealData) - 3):
            spreadSheet.cell(row=i + 3, column=2).value = self.sealData[i+1]

        spreadSheet.cell(row=sealDataLength - 1, column=2).value = get_sex_str_from_int(int(float(self.sealData[sealDataLength - 2])))
        spreadSheet.cell(row=sealDataLength, column=2).value = get_seal_species_str_from_int(int(float(
            self.sealData[sealDataLength - 1])))
        spreadSheet.cell(row=sealDataLength + 1, column=2).value = get_chances_str_from_int(int(float(
            self.sealData[sealDataLength-1])))

        excelFile.save(import_path)

    # Load the default model
    def load_default_model(self):
        self.output_label.setText("")
        self.modelName = defaultModelName
        self.model = joblib.load(MODEL_PATH)
        self.featureList = defaultFeatureList
        self.reset_input_fields_text()
        self.update_input_and_labels()
        pop_message_box("Default model loaded successfully")

    # Load a model from the local machine
    def load_model(self):
        self.output_label.setText("")
        import_path = QFileDialog.getOpenFileName(filter='PKL files (*.pkl)')[0]
        if not (import_path == ""):
            self.model = joblib.load(import_path)
            fileName = Path(import_path).stem
            self.update_feature_list(fileName)
            self.reset_input_fields_text()
            self.update_input_and_labels()

    # if the result is zero, there´s a problem when taking the input
    def get_import(self):
        result = 0
        import_path_null = False
        import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
        # if you open the window file explorer and click cancel
        if import_path == "":
            import_path_null = True
        sex = get_sex_int(self.combo1.currentText())
        species = get_seal_species_int(self.combo2.currentText())
        if not import_path_null:
            result, self.sealData = make_prediction(import_path, sex, species, self.model, self.featureList)
            sealTag = self.get_seal_tag(import_path)
            if sealTag == "":
                pop_message_box("Check that the correct file is being uploaded and contains a seal tag")
                result = 0
            else:
                sealTag = "T" + sealTag
                self.sealData = np.concatenate((np.array([sealTag]), self.sealData), axis=0)
        if not (result == 0):
            self.output_label.setText("Seal tag - " + sealTag + "\n\n" + result)

    # retrieves the seal tag of the seal whose data is present in the file
    def get_seal_tag(self, import_path):
        new_seal_data = pd.read_excel(import_path).to_numpy()
        sealTag = np.where((new_seal_data == 'Rhb. number:') | (new_seal_data == 'Rhb. number: '))[0]
        tag = ""
        if not (np.where((new_seal_data == 'Rhb. number:') | (new_seal_data == 'Rhb. number: '))[0].size == 0):
            for i in range(1, 5):
                if not (pd.isnull(new_seal_data[sealTag[0]][i])):
                    tag = new_seal_data[sealTag[0]][i]
        return tag

    def run_prediction(self):
        sex = get_sex_int(self.combo1.currentText())
        species = get_seal_species_int(self.combo2.currentText())
        data = []
        try:
            for feature in self.featureList:
                data = np.append(data, [float(self.featureInputDict.get(feature).text())])
            result, survival = find_prediction(data, self.model, sex, species)
            self.output_label.setText(result)
        except ValueError as ve1:
            pop_message_box(
                "Something went wrong.\nCheck that you filled in all the boxes only entered numbers.\nMake sure to write decimals with a dot ( . ) and not a comma ( , )")