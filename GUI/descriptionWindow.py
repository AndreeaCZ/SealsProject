from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

from GUI.utils import lightgray

string = open('description.txt').read()


# Represents the description window of the application
class DescriptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(800, 400))
        layout = QVBoxLayout()
        text = QTextEdit()
        text.setMarkdown(string)
        text.setReadOnly(True)
        layout.addWidget(text)
        self.setLayout(layout)
        self.setAutoFillBackground(True)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)


        # VERSION WITH PICTURES, WILL PROBABLY REMOVE LATER
        # layout = QVBoxLayout()
        # text = QTextEdit()
        # text.setMarkdown(string)
        # text.setReadOnly(True)
        # text.setFixedHeight(1000)
        # layout.addWidget(text)
        # layout.addStretch()
        # image = QLabel()
        # pic = QPixmap.fromImage(QImage('/Users/andreeazelko/Documents/SoftwareEngineering/SealsProject/treeOutput.png'))
        # image.setPixmap(pic.scaledToWidth(600))
        # layout.addWidget(image)
        # inWidget = QWidget()
        # inWidget.setLayout(layout)
        # scroll = QScrollArea()
        # scroll.setWidget(inWidget)
        # outsideLayout = QVBoxLayout()
        # outsideLayout.addWidget(scroll)
        # self.setLayout(outsideLayout)
