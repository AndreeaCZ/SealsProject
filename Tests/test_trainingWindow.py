import sys
import unittest
from unittest import TestCase, mock

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.trainingWindow import TrainModelWindow

app = QApplication(sys.argv)

class TestAddSealWindow(TestCase):
    # SET UP:
    # Open window and attach bot to window
    def setUp(self):

        m = mock.Mock()
        self.test_window = TrainModelWindow(m)
        # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Train a model"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(500, 450))

    def test_train_button_clicked(self):
        with mock.patch('GUI.trainingWindow.TrainModelWindow.train_new_model') as clickCheck:
            m = mock.Mock()
            test_window = TrainModelWindow(m)
            train_button = test_window.train_button
            QTest.mouseClick(train_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_save_button_clicked(self):
        with mock.patch('GUI.trainingWindow.TrainModelWindow.save_model') as clickCheck:
            m = mock.Mock()
            test_window = TrainModelWindow(m)
            save_button = test_window.save_button
            QTest.mouseClick(save_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.trainingWindow.TrainModelWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = TrainModelWindow(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

if __name__ == '__main__':
    unittest.main()


