from PyQt6.QtCore import QSize, QUrl, QVariant, QByteArray
from PyQt6.QtGui import QTextDocument, QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QScrollArea
from PIL import Image

string = open('description.txt').read()


class DescriptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(800, 400))
        layout = QVBoxLayout()
        text = QTextEdit()
        text.setMarkdown(string)
        text.setReadOnly(True)
        text.setFixedHeight(1000)
        layout.addWidget(text)
        layout.addStretch()
        image = QLabel()
        pic = QPixmap.fromImage(QImage('/Users/andreeazelko/Documents/SoftwareEngineering/SealsProject/treeOutput.png'))
        image.setPixmap(pic.scaledToWidth(600))
        layout.addWidget(image)
        inWidget = QWidget()
        inWidget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(inWidget)
        outsideLayout = QVBoxLayout()
        outsideLayout.addWidget(scroll)
        self.setLayout(outsideLayout)
