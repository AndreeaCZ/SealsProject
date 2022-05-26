import joblib
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import *
from GUI.utils import *
from variables import MODEL_PATH


class PredictionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.result = 0
        self.model = joblib.load(MODEL_PATH)
        self.setWindowTitle("Run predictions")
        self.setFixedSize(QSize(700, 400))
        self.layout = QGridLayout()

        # Creating elements:
        self.input_line = QLineEdit()
        self.import_button = QPushButton('Import')
        self.output_label = QLabel()
        self.save_button = QPushButton('Save')
        self.image_label = QLabel()
        self.load_model_button = QPushButton('Load a model')
        self.load_default_model_button = QPushButton('Default model')
        # Creating import sub fields
        self.combo1 = QComboBox()
        self.combo1.addItem("Female")
        self.combo1.addItem("Male")
        self.combo2 = QComboBox()
        self.combo2.addItem("Phoca Vitulina")
        self.combo2.addItem("Halichoerus Grypus")

        # Set widget properties:
        self.setAutoFillBackground(True)
        self.set_elements()
        self.setLayout(self.layout)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)

    def set_elements(self):
        # Setting elements properties:
        self.input_line.setFixedWidth(300)
        self.input_line.setPlaceholderText('File Path')
        self.import_button.clicked.connect(self.get_import)
        self.output_label.setText('Enter data to see prediction')
        self.load_model_button.clicked.connect(self.load_model)
        self.load_default_model_button.clicked.connect(self.load_default_model)
        self.save_button.clicked.connect(self.save_results)
        # Adding elements to input layout:
        self.layout.addWidget(self.combo1, 1, 0, 1, 2)
        self.layout.addWidget(self.combo2, 2, 0, 1, 2)
        self.layout.addWidget(self.input_line, 3, 0, 1, 2)
        self.layout.addWidget(self.import_button, 3, 2)
        self.layout.addWidget(self.load_default_model_button, 1,2)
        self.layout.addWidget(self.load_model_button, 2, 2)
        self.layout.addWidget(self.output_label, 4, 0, 1, 2)
        self.layout.addWidget(self.save_button, 4, 2)
        self.layout.setRowStretch(5, 1)
        self.layout.setRowMinimumHeight(3, 100)
        self.layout.setRowMinimumHeight(4, 100)

    def save_results(self):
        print(self.result)

    # Load the default model
    def load_default_model(self):
        self.model = joblib.load(MODEL_PATH)
        msgBox = QMessageBox()
        msgBox.setText("Default model loaded successfully")
        msgBox.exec()

    # Load a model from the local machine
    def load_model(self):
        import_path = QFileDialog.getOpenFileName(filter='PKL files (*.pkl)')[0]
        if not (import_path == ""):
            self.model = joblib.load(import_path)
            msgBox = QMessageBox()
            msgBox.setText("Model loaded successfully")
            msgBox.exec()
            print(import_path)

    # if the result is zero, there´s a problem when taking the input
    def get_import(self):
        import_path = self.input_line.text()
        import_path_null = True
        if not import_path:
            import_path_null = False;
            import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
            # if you open the window file explorer and click cancel
            if import_path == "":
                import_path_null = True;
        sex = self.combo1.currentText()
        species = self.combo2.currentText()
        sex1 = getSexInt(sex)
        species1 = getSealSpeciesInt(species)
        if not import_path_null:
            self.result = make_prediction(import_path, sex1, species1, self.model)
        if not (self.result == 0):
            self.output_label.setText(self.result)

def getSealSpeciesInt(str):
        if str == "Phoca Vitulina":
            return 0
        if str == "Halichoerus Grypus":
            return 1

def getSexInt(str):
        if str == "Female":
            return 0
        if str == "Male":
            return 1
