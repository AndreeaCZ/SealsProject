from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import *
from openpyxl import load_workbook
from Model.modelFunctions import *
from Database.modelDataGeneration import get_model_data
from GUI.utils import lightgray, pop_message_box
from variables import DIV

########################################################################################################################
# Represents the window that lets the user train their own model
########################################################################################################################


# TODO: Please rename this and explain what it does
maxNumOfExcludedFeatures = 12


class TrainModelWindow(QWidget):
    def __init__(self, dashboard):
        super().__init__()
        self.model = None
        self.excelRowIndex = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.setFixedSize(QSize(500, 400))
        self.setWindowTitle("Train a model")
        # close home page
        self.dashboard = dashboard
        dashboard.close()

        # Creating a home button
        self.home_button = QPushButton('Home')

        # Creating elements
        self.sex = QCheckBox("Sex")
        self.species = QCheckBox("Species")
        self.wbc = QCheckBox("WBC")
        self.lymf = QCheckBox("LYMF")
        self.gran = QCheckBox("GRAN")
        self.mid = QCheckBox("MID")
        self.rbc = QCheckBox("RBC")
        self.hgb = QCheckBox("HGB")
        self.mch = QCheckBox("MCH")
        self.mchc = QCheckBox("MCHC")
        self.mpv = QCheckBox("MPV")
        self.plt = QCheckBox("PLT")
        self.accu_label = QLabel()
        self.train_button = QPushButton('Train')
        self.input_model_name = QLineEdit()
        self.save_button = QPushButton('Save')

        # Setting widget properties:
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
        # Setting elements:
        self.accu_label.setText("Model accuracy")
        self.input_model_name.setPlaceholderText("Enter model name")
        self.train_button.clicked.connect(self.train_new_model)
        self.save_button.clicked.connect(self.save_model)
        self.home_button.clicked.connect(self.go_to_home)
        # Adding elements to the layout:
        layout = QVBoxLayout()
        layout.addWidget(self.sex)
        layout.addWidget(self.species)
        layout.addWidget(self.wbc)
        layout.addWidget(self.lymf)
        layout.addWidget(self.gran)
        layout.addWidget(self.mid)
        layout.addWidget(self.rbc)
        layout.addWidget(self.hgb)
        layout.addWidget(self.mch)
        layout.addWidget(self.mchc)
        layout.addWidget(self.mpv)
        layout.addWidget(self.plt)
        layout.addWidget(self.accu_label)
        layout.addWidget(self.train_button)
        layout.addWidget(self.input_model_name)
        layout.addWidget(self.save_button)
        layout.addWidget(self.home_button)
        return layout

    # Saves a user trained model
    def save_model(self):
        model_name = self.input_model_name.text()
        if model_name == "":
            pop_message_box("Please enter a model name.")
        else:
            # the user tries to save a model only after training it
            if not (self.model is None):
                import_path = QFileDialog.getExistingDirectoryUrl().path()
                if not (import_path == ""):
                    import_path = import_path + DIV + model_name + ".pkl"
                    # save the model details into the Excel file (featuresChecklist.xlsx)
                    isSuccessful = save_features(self.excelRowIndex, model_name)
                    if isSuccessful == 1:
                        joblib.dump(self.model, "D:\\save.pkl")
                        # pops a message box
                        pop_message_box("Model saved successfully")
                        self.model = None
            else:
                pop_message_box("Please train a model first.")
            self.input_model_name.setText("")

    # Trains a model based on the features selected
    def train_new_model(self):
        try:
            datasetLabeledSeals = get_model_data()

            # Features not included in training
            excludedFeaturesNum = 0
            self.excelRowIndex = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            # if a feature is unchecked, it is removed from the training model params
            if not self.sex.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['Sex'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(2)

            if not self.species.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['Species'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(3)

            if not self.wbc.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['WBC'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(4)
            if not self.lymf.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['LYMF'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(5)
            if not self.gran.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['GRAN'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(6)
            if not self.mid.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['MID'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(7)
            if not self.rbc.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['RBC'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(8)
            if not self.hgb.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['HGB'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(9)
            if not self.mch.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['MCH'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(10)
            if not self.mchc.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['MCHC'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(11)
            if not self.mpv.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['MPV'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(12)
            if not self.plt.isChecked():
                datasetLabeledSeals = datasetLabeledSeals.drop(['PLT'], axis=1)
                excludedFeaturesNum += 1
                self.excelRowIndex.remove(13)
        except Exception as e:
            pop_message_box("Failed to remove selected data")

        try:
            if excludedFeaturesNum != maxNumOfExcludedFeatures:
                X_train, X_test, y_train, y_test = data_preprocessing(datasetLabeledSeals)
                predictionModel = rf_Model()
                self.model = predictionModel.fit(X_train, y_train)

                self.accu_label.setText(
                    "Your new model's accuracy " + str(round(test_accuracy(predictionModel, X_test, y_test)* 100, 3)) + "%")
                pop_message_box("Model trained successfully")
            else:
                pop_message_box("Please select features to train on.")
        except Exception as e:
            pop_message_box("Failed to train model")


# This function is used to update the Excel file. This Excel file is used to note down all the selected features
# for the trained models. If a feature was used, then the corresponding cell will be filled with 1.
def save_features(rowIndexList, modelName):
    # load a workbook and worksheet.
    try:
        wb = load_workbook("featuresChecklist.xlsx")
        ws = wb.active
        colIndex = 2
        maxCol = ws.max_column
        maxRow = ws.max_row
        # Find the empty column
        for j in range(2, maxCol + 1):
            counter = 0
            for i in range(2, maxRow + 1):
                if ws.cell(row=i, column=j).value is None:
                    counter = counter + 1
            if counter == maxRow - 1:
                break
            else:
                colIndex = colIndex + 1
        # Check if a new column is needed
        if colIndex == maxCol:
            ws.insert_cols(maxCol + 1)
        # Fill in the corresponding values
        ws.cell(row=1, column=colIndex).value = modelName
        for i in rowIndexList:
            # fill in the cell with 1
            ws.cell(row=i, column=colIndex).value = 1
        wb.save("featuresChecklist.xlsx")
        return 1
    except:
        pop_message_box("Can't find the featuresChecklist.xlsx file")
    return 0
