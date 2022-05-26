import sys
import joblib
from PyQt6.QtCore import QSize
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from GUI.descriptionWindow import DescriptionWindow
from GUI.trainingWindow import TrainModelWindow
from GUI.predictionWindow import PredictionWindow
from GUI.addSealWindow import AddSealWindow
from GUI.getSealDataWindow import GetSealDataWindow
from GUI.utils import *
from variables import MODEL_PATH


app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = joblib.load(MODEL_PATH)
        self.setWindowTitle("Blubber")
        self.setFixedSize(QSize(700, 400))
        # Creating window elements:
        self.trainingWindow = None
        self.descriptionWindow = None
        self.predictionWindow = None
        self.addSealWindow = None
        self.getSealWindow = None

        # Creating left side elements:
        self.predict_button = QPushButton('Predict')
        self.data_ranges_button = QPushButton('Data Ranges')
        self.about_button = QPushButton('About')
        self.trainModel_button = QPushButton('Train Model')
        self.add_seal_button = QPushButton('Add a seal')
        self.get_seal_button = QPushButton('Get seal data')

        # Creating widgets:
        widget = self.make_left_side()

        self.setCentralWidget(widget)

    def make_left_side(self):
        self.predict_button.clicked.connect(self.open_prediction_window)
        self.about_button.clicked.connect(self.open_description_window)
        self.trainModel_button.clicked.connect(self.open_training_window)
        self.add_seal_button.clicked.connect(self.open_add_seal_window)
        self.get_seal_button.clicked.connect(self.open_get_seal_window)
        self.predict_button.setFixedHeight(150)
        self.data_ranges_button.setFixedHeight(150)
        self.about_button.setFixedHeight(150)
        self.trainModel_button.setFixedHeight(150)
        self.add_seal_button.setFixedHeight(150)
        self.get_seal_button.setFixedHeight(150)
        layout = QGridLayout()
        layout.addWidget(self.predict_button, 0, 0)
        layout.addWidget(self.data_ranges_button, 0, 1)
        layout.addWidget(self.about_button, 1,0)
        layout.addWidget(self.trainModel_button, 1, 1)
        layout.addWidget(self.add_seal_button, 2, 0)
        layout.addWidget(self.get_seal_button, 2, 1)
        widget = QWidget()
        widget.setAutoFillBackground(True)
        widget.setLayout(layout)
        p = widget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        widget.setPalette(p)
        return widget

    def open_training_window(self):
        self.trainingWindow = TrainModelWindow()
        self.trainingWindow.show()

    def open_description_window(self):
        self.descriptionWindow = DescriptionWindow()
        self.descriptionWindow.show()

    def open_prediction_window(self):
        self.predictionWindow = PredictionWindow()
        self.predictionWindow.show()

    def open_add_seal_window(self):
        self.addSealWindow = AddSealWindow()
        self.addSealWindow.show()

    def open_get_seal_window(self):
        self.getSealWindow = GetSealDataWindow()
        self.getSealWindow.show()


window = MainWindow()
window.show()

app.exec()
