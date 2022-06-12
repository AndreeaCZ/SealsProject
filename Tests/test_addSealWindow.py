import sys
import unittest
from unittest import TestCase, mock
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
from GUI.addSealWindow import AddSealWindow

app = QApplication(sys.argv)


class TestAddSealWindow(TestCase):
    # SET UP:
    # Open window and attach bot to window
    def setUp(self):
        m = mock.Mock()
        self.test_window = AddSealWindow(m)

        # TestInitial: title, size , button clicked working?

    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Add a seal"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(700, 400))

    def test_add_button_clicked(self):
        with mock.patch('GUI.addSealWindow.AddSealWindow.add_seal') as clickCheck:
            m = mock.Mock()
            test_window = AddSealWindow(m)
            add_button = test_window.addSeal_button
            QTest.mouseClick(add_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.addSealWindow.AddSealWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = AddSealWindow(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

if __name__ == '__main__':
    unittest.main()
