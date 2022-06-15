import sys
import joblib
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout

from GUI.addSealWindow import AddSealWindow
from GUI.descriptionWindow import DescriptionWindow
from GUI.getSealDataWindow import GetSealDataWindow
from GUI.predictionWindow import PredictionWindow
from GUI.queryDatabaseWindow import QueryDatabaseWindow
from GUI.trainingWindow import TrainModelWindow
from GUI.aboutPage import About
from GUI.utils import darkgray
from variables import MODEL_PATH

########################################################################################################################
# Represents the main (initial) window of the application
########################################################################################################################

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = joblib.load(MODEL_PATH)
        self.setWindowTitle("Blubber")
        self.setFixedSize(QSize(700, 450))

        # Creating window elements:
        self.trainingWindow = None
        self.user_guideWindow = None
        self.predictionWindow = None
        self.addSealWindow = None
        self.getSealWindow = None
        self.queryDatabaseWindow = None
        self.aboutWindow = None

        # Creating left side elements:
        self.predict_button = QPushButton('Predict')
        self.query_database_button = QPushButton('Query the database')
        self.user_guide = QPushButton('User Guide')
        self.trainModel_button = QPushButton('Train Model')
        self.add_seal_button = QPushButton('Add a seal')
        self.get_seal_button = QPushButton('Get seal data')
        self.about_button = QPushButton('About the model')

        # Creating widgets:
        widget = self.set_elements()

        self.setCentralWidget(widget)

    def set_elements(self):
        """
        Sets the elements of the window
        :return: the layout of the window
        """
        # Setting elements:
        self.predict_button.clicked.connect(self.open_prediction_window)
        self.user_guide.clicked.connect(self.open_description_window)
        self.trainModel_button.clicked.connect(self.open_training_window)
        self.add_seal_button.clicked.connect(self.open_add_seal_window)
        self.get_seal_button.clicked.connect(self.open_get_seal_window)
        self.query_database_button.clicked.connect(self.open_query_database_window)
        self.about_button.clicked.connect(self.open_about_window)
        self.predict_button.setFixedHeight(100)
        self.query_database_button.setFixedHeight(100)
        self.user_guide.setFixedHeight(100)
        self.trainModel_button.setFixedHeight(100)
        self.add_seal_button.setFixedHeight(100)
        self.get_seal_button.setFixedHeight(100)
        self.about_button.setFixedHeight(100)

        # Adding elements to layout:
        layout = QGridLayout()
        layout.addWidget(self.predict_button, 0, 0)
        layout.addWidget(self.query_database_button, 0, 1)
        layout.addWidget(self.user_guide, 1, 0)
        layout.addWidget(self.trainModel_button, 1, 1)
        layout.addWidget(self.add_seal_button, 2, 0)
        layout.addWidget(self.get_seal_button, 2, 1)
        layout.addWidget(self.about_button, 3, 0)
        # Setting widget properties:
        widget = QWidget()
        widget.setAutoFillBackground(True)
        widget.setLayout(layout)
        p = widget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        widget.setPalette(p)
        return widget

    def open_query_database_window(self):
        self.queryDatabaseWindow = QueryDatabaseWindow(window)
        self.queryDatabaseWindow.show()

    def open_training_window(self):
        self.trainingWindow = TrainModelWindow(window)
        self.trainingWindow.show()

    def open_description_window(self):
        self.descriptionWindow = DescriptionWindow(window)
        self.descriptionWindow.show()

    def open_prediction_window(self):
        self.predictionWindow = PredictionWindow(window)
        self.predictionWindow.show()

    def open_add_seal_window(self):
        self.addSealWindow = AddSealWindow(window)
        self.addSealWindow.show()

    def open_get_seal_window(self):
        self.getSealWindow = GetSealDataWindow(window)
        self.getSealWindow.show()

    def open_about_window(self):
        self.aboutWindow = About(window)
        self.aboutWindow.show()


window = MainWindow()
window.show()

app.exec()
