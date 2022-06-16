import sys
import unittest
from unittest import TestCase, mock

from PyQt6.QtCore import Qt, QSize, qDebug
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from GUI.trainingWindow import TrainModelWindow

########################################################################################################################
# File for testing the training window
########################################################################################################################
from Model.modelCreation import data_preprocessing

app = QApplication(sys.argv)


class TestTrainingWindow(TestCase):
    # SET UP:
    # Opening dummyDB for testing is not implemented yet.
    # If dummbyDB executed, all data in dummbyDB will be deleted and the DB will be closed when the tests ended.
    def setUp(self):
        m = mock.Mock()
        self.test_window = TrainModelWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), "Train a model")


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
            self.assertTrue(clickCheckgit .called)

    @mock.patch("joblib.load")
    @mock.patch("GUI.trainingWindow.pop_message_box")
    def test_train_new_model(self ,mock_load, mock_pop):
        # Before training a model, the model should be set to none
        self.assertIsNone(self.test_window.model)

        # Train new model with wbc
        self.test_window.wbc.click()
        self.assertTrue(self.test_window.wbc.isChecked())
        self.test_window.train_new_model()
        self.assertIsNotNone(self.test_window.model)

    @mock.patch("joblib.load")
    @mock.patch("GUI.trainingWindow.pop_message_box")
    def test_display_confusion_matrix(self,mock_load, mock_pop):
        # Choosing features
        self.test_window.wbc.click()
        self.test_window.lymf.click()
        self.test_window.gran.click()
        self.test_window.mid.click()
        self.test_window.rbc.click()

        # After training the model, confusion matrix should not be empty
        self.assertIs(self.test_window.confusion_matrix.text(),"")
        self.test_window.train_new_model()
        self.assertIsNot(self.test_window.confusion_matrix.text(),"")

    @mock.patch("joblib.load")
    @mock.patch("GUI.trainingWindow.pop_message_box")
    def test_display_feature_importance(self,mock_load, mock_pop):
        # Choosing features
        self.test_window.mch.click()
        self.test_window.lymf.click()
        self.test_window.gran.click()
        self.test_window.hgb.click()
        self.test_window.rbc.click()

        # After training the model, feature importance should not be empty
        self.assertEqual(self.test_window.feature_importance.text(),"Feature importance")
        self.test_window.train_new_model()
        self.assertNotEqual(self.test_window.feature_importance.text(),"Feature importance")


if __name__ == '__main__':
    unittest.main()
