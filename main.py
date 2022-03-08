import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seals blood data analysis")
        self.setFixedSize(QSize(700, 400))

        # LEFT SIDE:

        homeButton = QPushButton('Home')
        dataRangesButton = QPushButton('Data Ranges')
        aboutButton = QPushButton('About')

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(homeButton)
        leftLayout.addWidget(dataRangesButton)
        leftLayout.addWidget(aboutButton)
        leftLayout.addStretch()

        leftWidget = QWidget()
        leftWidget.setAutoFillBackground(True)
        leftWidget.setFixedWidth(200)
        leftWidget.setLayout(leftLayout)
        p = leftWidget.palette()
        p.setColor(QPalette.ColorRole.Window, QColor('#095056'))
        leftWidget.setPalette(p)

        # RIGHT SIDE:

        inputLine = QLineEdit()
        inputLine.setFixedWidth(300)
        inputLine.setPlaceholderText('Input')

        importButton = QPushButton('Import')
        importButton.setAttribute

        outputLabel = QLabel()
        outputLabel.setText('Yes / No is the seals dead')

        saveButton = QPushButton('Save')

        imageLabel = QLabel()
        pic = QPixmap('fancyGraph.png').scaledToHeight(250)
        imageLabel.setPixmap(pic)

        rightLayout = QGridLayout()
        rightLayout.addWidget(inputLine, 0, 0)
        rightLayout.addWidget(importButton, 0, 1)
        rightLayout.addWidget(outputLabel, 1, 0)
        rightLayout.addWidget(saveButton, 1, 1)
        rightLayout.addWidget(imageLabel, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        rightWidget = QWidget()
        rightWidget.setAutoFillBackground(True)
        rightWidget.setLayout(rightLayout)
        q = rightWidget.palette()
        q.setColor(QPalette.ColorRole.Window, QColor('#669fa8'))
        rightWidget.setPalette(q)

        layout = QGridLayout()
        layout.addWidget(leftWidget, 0, 0)
        layout.addWidget(rightWidget, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()