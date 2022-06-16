from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

from GUI.utils import lightgray
from variables import DESCRIPTION_PATH

########################################################################################################################
# Represents the description window of the application, contains the user guide that details all Blubber functionality
########################################################################################################################


class DescriptionWindow(QWidget):
    def __init__(self, dashboard):
        super().__init__()
        self.setFixedSize(QSize(800, 500))
        self.setWindowTitle('User Guide')
        #close the home page
        self.dashboard = dashboard
        dashboard.close()
        # Creating elements:
        self.text = QTextEdit()

        # Creating a home button
        self.home_button = QPushButton('Home')

        # Setting widget properties:
        self.setLayout(self.set_properties())
        self.setAutoFillBackground(True)
        q = self.palette()
        q.setColor(QPalette.ColorRole.Window, QColor(lightgray))
        self.setPalette(q)

    # re-opens the dashboard and closes the current window
    def go_to_home(self):
        """
        re-opens the dashboard and closes the current window
        """
        self.dashboard.show()
        self.close()

    def set_properties(self):
        """
        Sets the elements of the window
        :return: the layout of the window
        """
        # Setting elements:
        self.home_button.clicked.connect(self.go_to_home)
        self.text.setMarkdown(open(DESCRIPTION_PATH).read())
        self.text.setReadOnly(True)
        # Adding elements to layout:
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.home_button)
        return layout
