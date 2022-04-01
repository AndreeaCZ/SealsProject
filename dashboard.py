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
        # Setting element properties
        self.input_line.setFixedWidth(300)
        self.input_line.setPlaceholderText('Input')
        self.import_button.clicked.connect(self.get_import)
        self.output_label.setText('Yes / No is the seals dead')
        pic = QPixmap('fancyGraph.png').scaledToHeight(250)
        self.image_label.setPixmap(pic)
        # Adding the elements to layout:
        right_layout = QGridLayout()
        right_layout.addWidget(self.input_line, 0, 0)
        right_layout.addWidget(self.import_button, 0, 1)
        right_layout.addWidget(self.output_label, 1, 0)
        right_layout.addWidget(self.save_button, 1, 1)
        right_layout.addWidget(self.image_label, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        # Setting properties:
        right_widget = QWidget()
        right_widget.setAutoFillBackground(True)
        right_widget.setLayout(right_layout)
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
                     get_data(new_seal_data, 'LYMF', True)]
    predictionArr = np.array(blood_results).reshape(1, -1)
    compare = int(SealDecisionTree.predict(predictionArr))
    if compare == 1:
        return "Will survive"
    else:
        return "Will not survive"


window = MainWindow()
window.show()

app.exec()
