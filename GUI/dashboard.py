import sys
import joblib
from PyQt6.QtCore import QSize
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from GUI.descriptionWindow import DescriptionWindow
from GUI.trainingWindow import TrainModelWindow
from GUI.predictionWindow import PredictionWindow
from GUI.databaseWindow import DatabaseWindow
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
        self.databaseWindow = None

        # Creating left side elements:
        self.predict_button = QPushButton('Predict')
        self.data_ranges_button = QPushButton('Data Ranges')
        self.about_button = QPushButton('About')
        self.trainModel_button = QPushButton('Train Model')
        self.database_button = QPushButton('Database')

        # Creating widgets:
        widget = self.make_left_side()

        self.setCentralWidget(widget)

    def make_left_side(self):
        self.predict_button.clicked.connect(self.open_prediction_window)
        self.about_button.clicked.connect(self.open_description_window)
        self.trainModel_button.clicked.connect(self.open_training_window)
        self.database_button.clicked.connect(self.open_database_window)
        self.predict_button.setFixedHeight(150)
        self.data_ranges_button.setFixedHeight(150)
        self.about_button.setFixedHeight(150)
        self.trainModel_button.setFixedHeight(150)
        self.database_button.setFixedHeight(150)
        layout = QGridLayout()
        layout.addWidget(self.predict_button, 0, 0)
        layout.addWidget(self.data_ranges_button, 0, 1)
        layout.addWidget(self.about_button, 1,0)
        layout.addWidget(self.trainModel_button, 1, 1)
        layout.addWidget(self.database_button, 2, 0)
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

    def open_database_window(self):
        self.databaseWindow = DatabaseWindow()
        self.databaseWindow.show()


window = MainWindow()
window.show()

app.exec()
