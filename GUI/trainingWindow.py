from sqlite3 import connect

import joblib
import pandas as pd
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from variables import DB_PATH, DIV


class TrainModelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = None
        self.setFixedSize(QSize(500, 300))
        layout = QVBoxLayout()
        self.setWindowTitle("Train a model")
        self.wbc = QCheckBox("WBC")
        self.lymf = QCheckBox("LYMF")
        self.rbc = QCheckBox("RBC")
        self.hgb = QCheckBox("HGB")
        self.mch = QCheckBox("MCH")
        self.mchc = QCheckBox("MCHC")
        self.mpv = QCheckBox("MPV")
        self.plt = QCheckBox("PLT")
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

        if not self.wbc.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['WBC'], axis=1)  # drop tag column
        if not self.lymf.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['LYMF'], axis=1)  # drop tag column
        if not self.rbc.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['RBC'], axis=1)  # drop tag column
        if not self.hgb.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['HGB'], axis=1)  # drop tag column
        if not self.mch.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['MCH'], axis=1)  # drop tag column
        if not self.mchc.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['MCHC'], axis=1)  # drop tag column
        if not self.mpv.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['MPV'], axis=1)  # drop tag column
        if not self.plt.isChecked():
            datasetLabeledSeals = datasetLabeledSeals.drop(['PLT'], axis=1)  # drop tag column

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
        # pops a message box
        self.popMessageBox("Model trained successfully")

