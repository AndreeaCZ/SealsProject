import sys
import unittest
from unittest import TestCase, mock

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from GUI.trainingWindow import *

app = QApplication(sys.argv)

class TestTraingWindow(TestCase):
    # SET UP:
    # Opening dummyDB for testing is not implemented yet.
    # If dummbyDB executed, all data in dummbyDB will be deleted and the DB will be closed when the tests ended.
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
            trainButton = test_window.train_button
            QTest.mouseClick(trainButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_save_button_clicked(self):
        with mock.patch('GUI.trainingWindow.TrainModelWindow.save_model') as clickCheck:
            m = mock.Mock()
            test_window = TrainModelWindow(m)
            saveButton = test_window.save_button
            QTest.mouseClick(saveButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.trainingWindow.TrainModelWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = TrainModelWindow(m)
            homeButton = test_window.home_button
            QTest.mouseClick(homeButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    # 1. test training a new model with checked parameters.
    # NOT IMPLEMENTED YET
    def test_train_new_model(self):
        self.fail()

    # 2. test saving the training model into a local repository.
    # NOT IMPLEMENTED YET
    def test_save_features(self):
        self.fail()

    # 3. test saving the training model without name.
    # NOT IMPLEMENTED YET
    def test_empty_model_name(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()


