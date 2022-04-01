import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blubber")
        self.setFixedSize(QSize(700, 400))

        # LEFT SIDE:

        home_button = QPushButton('Home')
        data_ranges_button = QPushButton('Data Ranges')
        about_button = QPushButton('About')

        left_layout = QVBoxLayout()
        left_layout.addWidget(home_button)
        left_layout.addWidget(data_ranges_button)
        left_layout.addWidget(about_button)
        left_layout.addStretch()

        left_widget = QWidget()
        left_widget.setAutoFillBackground(True)
        left_widget.setFixedWidth(200)
        left_widget.setLayout(left_layout)
        p = left_widget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(darkgray))
        left_widget.setPalette(p)

        # RIGHT SIDE:

        input_line = QLineEdit()
        input_line.setFixedWidth(300)
        input_line.setPlaceholderText('Input')

        import_button = QPushButton('Import')

        output_label = QLabel()
        output_label.setText('Yes / No is the seals dead')

        save_button = QPushButton('Save')

        image_label = QLabel()
        pic = QPixmap('fancyGraph.png').scaledToHeight(250)
        image_label.setPixmap(pic)

        right_layout = QGridLayout()
        right_layout.addWidget(input_line, 0, 0)
        right_layout.addWidget(import_button, 0, 1)
        right_layout.addWidget(output_label, 1, 0)
        right_layout.addWidget(save_button, 1, 1)
        right_layout.addWidget(image_label, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        right_widget = QWidget()
        right_widget.setAutoFillBackground(True)
        right_widget.setLayout(right_layout)
        q = right_widget.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        right_widget.setPalette(q)

        layout = QGridLayout()
        layout.addWidget(left_widget, 0, 0)
        layout.addWidget(right_widget, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
