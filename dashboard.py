import sys
import joblib
import pandas as pd
import numpy as np
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from dataParser import get_data

darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'

SealDecisionTree = joblib.load('SealDecisionTree.pkl')  # load the model created in the training phase

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    # Creating left side elements:
    home_button = QPushButton('Home')
    data_ranges_button = QPushButton('Data Ranges')
    about_button = QPushButton('About')
    # Creating right side elements:
    input_line = QLineEdit()
    import_button = QPushButton('Import')
    output_label = QLabel()
    save_button = QPushButton('Save')
    image_label = QLabel()
    # Creating input elements
    wbc_input = QLineEdit()
    lymf_input = QLineEdit()
    lymf_perc_input = QLineEdit()
    wbc_label = QLabel()
    lymf_label = QLabel()
    lymf_perc_label = QLabel()
    submit_button = QPushButton('Submit')

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
        self.wbc_label.setText('WBC')
        self.lymf_label.setText('LYMF')
        self.lymf_perc_label.setText('LYMF %')
        self.submit_button.clicked.connect(self.values_entered)
        # Setting element properties
        self.input_line.setFixedWidth(300)
        self.input_line.setPlaceholderText('File Path')
        self.import_button.clicked.connect(self.get_import)
        self.output_label.setText('Enter data to see prediction')
        # pic = QPixmap('fancyGraph.png').scaledToHeight(250)
        # self.image_label.setPixmap(pic)

        # Adding elements to input layout
        input_layout = QGridLayout()
        input_layout.addWidget(self.wbc_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        input_layout.addWidget(self.lymf_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        input_layout.addWidget(self.lymf_perc_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        input_layout.addWidget(self.wbc_input, 1, 0)
        input_layout.addWidget(self.lymf_input, 1, 1)
        input_layout.addWidget(self.lymf_perc_input, 1, 2)
        input_layout.addWidget(self.submit_button, 2, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        input_layout.addWidget(self.input_line, 3, 0, 1, 2)
        input_layout.addWidget(self.import_button, 3, 2)
        input_layout.addWidget(self.output_label, 4, 0, 1, 2)
        input_layout.addWidget(self.save_button, 4, 2)
        input_layout.setRowStretch(5, 1)
        input_layout.setRowMinimumHeight(3, 100)

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


def make_prediction(file_path):
    new_seal_data = pd.read_excel(file_path).to_numpy()
    blood_results = [get_data(new_seal_data, 'WBC', False),
                     get_data(new_seal_data, 'LYMF', False),
                     get_data(new_seal_data, 'GRAN', False),
                     get_data(new_seal_data, 'MID', False),
                     get_data(new_seal_data, 'LYMF', True),
                     get_data(new_seal_data, 'GRAN', True),
                     get_data(new_seal_data, 'MID', True),
                     get_data(new_seal_data, 'HCT', False),
                     get_data(new_seal_data, 'MCV', False),
                     get_data(new_seal_data, 'RBC', False),
                     get_data(new_seal_data, 'HGB', False),
                     get_data(new_seal_data, 'MCH', False),
                     get_data(new_seal_data, 'MCHC', False),
                     get_data(new_seal_data, 'PLT', False)]
    return find_prediction(blood_results)


def find_prediction(data):
    predictionArr = np.array(data).reshape(1, -1)
    compare = int(SealDecisionTree.predict(predictionArr))
    if compare == 1:
        return "Will survive"
    else:
        return "Will not survive"


window = MainWindow()
window.show()

app.exec()
