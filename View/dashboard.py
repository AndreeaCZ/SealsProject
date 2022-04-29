import sys

import joblib
import pandas as pd
import numpy as np
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from sqlite3 import connect
from sklearn.preprocessing import MinMaxScaler
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from SealsProject.variables import MODEL_NAME, DB_PATH

darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'

SealDecisionTree = joblib.load(MODEL_NAME)  # load the model created in the training phase

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    # Creating left side elements:
    home_button = QPushButton('Home')
    data_ranges_button = QPushButton('Data Ranges')
    about_button = QPushButton('About')
    trainModel_button = QPushButton('Train Model')
    # Creating right side elements:
    input_line = QLineEdit()
    import_button = QPushButton('Import')
    output_label = QLabel()
    save_button = QPushButton('Save')
    image_label = QLabel()
    # Creating input elements
    #wbc_input = QLineEdit()
    #lymf_input = QLineEdit()
    #lymf_perc_input = QLineEdit()
    #wbc_label = QLabel()
    #lymf_label = QLabel()
    #lymf_perc_label = QLabel()
    #submit_button = QPushButton('Submit')

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blubber")
        self.setFixedSize(QSize(700, 400))

        # LEFT SIDE:
        # Adding the elements to layout:
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.home_button)
        left_layout.addWidget(self.data_ranges_button)
        left_layout.addWidget(self.about_button)
        left_layout.addWidget(self.trainModel_button)
        left_layout.addStretch()
        # Setting properties:
        left_widget = QWidget()
        left_widget.setAutoFillBackground(True)
        left_widget.setFixedWidth(200)
        left_widget.setLayout(left_layout)
        p = left_widget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        left_widget.setPalette(p)

        # RIGHT SIDE:
        # Setting input elements properties:
        #self.wbc_label.setText('WBC')
        #self.lymf_label.setText('LYMF')
        #self.lymf_perc_label.setText('LYMF %')
        #self.submit_button.clicked.connect(self.values_entered)
        # Setting element properties
        self.input_line.setFixedWidth(300)
        self.input_line.setPlaceholderText('File Path')
        self.import_button.clicked.connect(self.get_import)
        self.trainModel_button.clicked.connect(self.openNewWindow)
        self.output_label.setText('Enter data to see prediction')
        # self.image_label.setPixmap(pic)

        # Adding elements to input layout
        input_layout = QGridLayout()
        #input_layout.addWidget(self.wbc_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        #input_layout.addWidget(self.lymf_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        #input_layout.addWidget(self.lymf_perc_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        #input_layout.addWidget(self.wbc_input, 1, 0)
        #input_layout.addWidget(self.lymf_input, 1, 1)
        #input_layout.addWidget(self.lymf_perc_input, 1, 2)
        #input_layout.addWidget(self.submit_button, 2, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        input_layout.addWidget(self.input_line, 3, 0, 1, 2)
        input_layout.addWidget(self.import_button, 3, 2)
        input_layout.addWidget(self.output_label, 4, 0, 1, 2)
        input_layout.addWidget(self.save_button, 4, 2)
        input_layout.setRowStretch(5, 1)
        input_layout.setRowMinimumHeight(3, 100)
        input_layout.setRowMinimumHeight(4, 100)

        # Setting properties:
        right_widget = QWidget()
        right_widget.setAutoFillBackground(True)
        right_widget.setLayout(input_layout)
        q = right_widget.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        right_widget.setPalette(q)

        # Setting final window layout
        layout = QGridLayout()
        layout.addWidget(left_widget, 0, 0)
        layout.addWidget(right_widget, 0, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def openNewWindow(self):
        print("yuhh")
        self.newWindow = TrainModelWindow()
        self.newWindow.show()

    def values_entered(self):
        values = [float(self.wbc_input.text()), float(self.lymf_input.text()), float(self.lymf_perc_input.text())]
        result = find_prediction(values)
        self.output_label.setText(result)

    def get_import(self):
        import_path = self.input_line.text()
        if not import_path:
            import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
        result = make_prediction(import_path)
        self.output_label.setText(result)

class TrainModelWindow(QWidget):

        def __init__(self):
            super().__init__()
            self.setFixedSize(QSize(700, 400))
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
            self.train_button.clicked.connect(self.train_new_model)
            layout.addWidget(self.train_button)
            self.setLayout(layout)

        def train_new_model(self):
            conn = connect(DB_PATH)  # create
            # database connection
            datasetLabeledSeals = pd.read_sql('SELECT *  FROM sealPredictionData', conn)  # import data into dataframe
            datasetLabeledSeals = datasetLabeledSeals.drop(['sealTag', 'HCT', 'MCV'], axis=1)  # drop tag column

            if (not self.wbc.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['WBC'], axis=1)  # drop tag column
            if (not self.lymf.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['LYMF'], axis=1)  # drop tag column
            if (not self.rbc.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['RBC'], axis=1)  # drop tag column
            if (not self.hgb.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['HGB'], axis=1)  # drop tag column
            if (not self.mch.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['MCH'], axis=1)  # drop tag column
            if (not self.mchc.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['MCHC'], axis=1)  # drop tag column
            if (not self.mpv.isChecked()):
                datasetLabeledSeals = datasetLabeledSeals.drop(['MPV'], axis=1)  # drop tag column
            if (not self.plt.isChecked()):
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
            survivalDecisionTree = survivalDecisionTree.fit(X_train, y_train)  # train the model
            predictions = survivalDecisionTree.predict(X_test)  # make predictions on the test set
            self.accu_label.setText("Your new model's accuracy " + str(accuracy_score(y_test, predictions)) + "%")

def make_prediction(file_path):
    new_seal_data = pd.read_excel(file_path).to_numpy()

    colNumber = np.where(new_seal_data == "LOW")[1][0]

    WBC = new_seal_data[np.where(new_seal_data == "WBC")[0][0]][colNumber]
    LYMF = new_seal_data[np.where(new_seal_data == "LYMF")[0][0]][colNumber]
    RBC = new_seal_data[np.where(new_seal_data == "RBC")[0][0]][colNumber]
    HGB = new_seal_data[np.where(new_seal_data == "HGB")[0][0]][colNumber]
    MCH = new_seal_data[np.where(new_seal_data == "MCH")[0][0]][colNumber]
    MCHC = new_seal_data[np.where(new_seal_data == "MCHC")[0][0]][colNumber]
    MPV = new_seal_data[np.where(new_seal_data == "MPV")[0][0]][colNumber]
    PLT = new_seal_data[np.where(new_seal_data == "PLT")[0][0]][colNumber]

    blood_results = [WBC, LYMF, RBC, HGB, MCH, MCHC, MPV, PLT]
    return find_prediction(blood_results)


def find_prediction(data):
    predictionArr = np.array(data).reshape(1, -1)
    compare = int(SealDecisionTree.predict(predictionArr))
    output = "Values you entered:\n" + ", ".join(map(str, data)) + "\n\nModel prediction:\n"
    if compare == 1:
        return output + "Will survive"
    else:
        return output + "Will not survive"


window = MainWindow()
window.show()

app.exec()
