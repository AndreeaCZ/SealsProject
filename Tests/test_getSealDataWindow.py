import sys
from unittest import TestCase, mock

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.getSealDataWindow import *

app = QApplication(sys.argv)

class TestGetSealDataWindow(TestCase):
    # SET UP:
    def setUp(self):
        m = mock.Mock()
        self.test_window = GetSealDataWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Get seal data"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(700, 500))

    def test_get_button_clicked(self):
        with mock.patch('GUI.getSealDataWindow.GetSealDataWindow.get_seal_data') as clickCheck:
            m = mock.Mock()
            test_window = GetSealDataWindow(m)
            getButton = test_window.getSealData_button
            QTest.mouseClick(getButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.getSealDataWindow.GetSealDataWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = GetSealDataWindow(m)
            homeButton = test_window.home_button
            QTest.mouseClick(homeButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_show_seal_data(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()
