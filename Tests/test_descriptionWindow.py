import sys
import unittest
from unittest import TestCase, mock

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.descriptionWindow import DescriptionWindow

########################################################################################################################
# File for testing the description window
########################################################################################################################


app = QApplication(sys.argv)


class TestDescription(TestCase):
    # SET UP:
    def setUp(self):
        m = mock.Mock()
        self.test_window = DescriptionWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), "User Guide")

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(800, 500))

    def test_button_clicked(self):
        with mock.patch('GUI.descriptionWindow.DescriptionWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = DescriptionWindow(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)


if __name__ == '__main__':
    unittest.main()
