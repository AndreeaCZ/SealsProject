import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from GUI.trainingWindow import TrainModelWindow
from GUI.descriptionWindow import DescriptionWindow
from GUI.utils import *

darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blubber")
        self.setFixedSize(QSize(700, 400))

        # Creating window elements:
        self.trainingWindow = None
        self.descriptionWindow = None

        # Creating left side elements:
        self.home_button = QPushButton('Home')
        self.data_ranges_button = QPushButton('Data Ranges')
        self.about_button = QPushButton('About')
        self.trainModel_button = QPushButton('Train Model')

        # Creating input elements:
        self.wbc_input = QLineEdit()
        self.lymf_input = QLineEdit()
        self.lymf_perc_input = QLineEdit()
        self.wbc_label = QLabel()
        self.lymf_label = QLabel()
        self.lymf_perc_label = QLabel()
        self.submit_button = QPushButton('Submit')

        # Creating right side elements:
        self.input_line = QLineEdit()
        self.import_button = QPushButton('Import')
        self.output_label = QLabel()
        self.save_button = QPushButton('Save')
        self.image_label = QLabel()

        # Creating widgets:
        left_widget = self.make_left_side()
        self.right_layout = QGridLayout()
        right_widget = self.make_right_side()

        # Creating overall layout:
        layout = QGridLayout()
        layout.addWidget(left_widget, 0, 0)
        layout.addWidget(right_widget, 0, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def make_left_side(self):
        self.about_button.clicked.connect(self.open_description_window)
        self.trainModel_button.clicked.connect(self.open_training_window)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.home_button)
        left_layout.addWidget(self.data_ranges_button)
        left_layout.addWidget(self.about_button)
        left_layout.addWidget(self.trainModel_button)
        left_layout.addStretch()
        left_widget = QWidget()
        left_widget.setAutoFillBackground(True)
        left_widget.setFixedWidth(200)
        left_widget.setLayout(left_layout)
        p = left_widget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        left_widget.setPalette(p)
        return left_widget

    def make_right_side(self):
        # self.set_input_elements()
        # Toggle this ^ to have value input elements
        self.set_right_side_elements()
        right_widget = QWidget()
        right_widget.setAutoFillBackground(True)
        right_widget.setLayout(self.right_layout)
        q = right_widget.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        right_widget.setPalette(q)
        return right_widget

    def set_input_elements(self):
        # Setting input elements properties:
        self.wbc_label.setText('WBC')
        self.lymf_label.setText('LYMF')
        self.lymf_perc_label.setText('LYMF %')
        self.submit_button.clicked.connect(self.values_entered)
        # Adding elements to input layout:
        self.right_layout.addWidget(self.wbc_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.lymf_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.lymf_perc_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.wbc_input, 1, 0)
        self.right_layout.addWidget(self.lymf_input, 1, 1)
        self.right_layout.addWidget(self.lymf_perc_input, 1, 2)
        self.right_layout.addWidget(self.submit_button, 2, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

    def set_right_side_elements(self):
        # Setting right side elements properties:
        self.input_line.setFixedWidth(300)
        self.input_line.setPlaceholderText('File Path')
        self.import_button.clicked.connect(self.get_import)
        self.output_label.setText('Enter data to see prediction')
        # Adding elements to input layout:
        self.right_layout.addWidget(self.input_line, 3, 0, 1, 2)
        self.right_layout.addWidget(self.import_button, 3, 2)
        self.right_layout.addWidget(self.output_label, 4, 0, 1, 2)
        self.right_layout.addWidget(self.save_button, 4, 2)
        self.right_layout.setRowStretch(5, 1)
        self.right_layout.setRowMinimumHeight(3, 100)
        self.right_layout.setRowMinimumHeight(4, 100)

    def open_training_window(self):
        self.trainingWindow = TrainModelWindow()
        self.trainingWindow.show()

    def open_description_window(self):
        self.descriptionWindow = DescriptionWindow()
        self.descriptionWindow.show()


    def values_entered(self):
        values = [float(self.wbc_input.text()), float(self.lymf_input.text()), float(self.lymf_perc_input.text())]
        result = find_prediction(values)
        self.output_label.setText(result)

    def get_import(self):
        import_path = self.input_line.text()
        if not import_path:
            import_path = QFileDialog.getOpenFileName(filter='Excel files (*.xlsx)')[0]
        print(import_path)
        result = make_prediction(import_path)
        self.output_label.setText(result)


window = MainWindow()
window.show()

app.exec()
