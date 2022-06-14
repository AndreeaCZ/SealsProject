import sys
from unittest import TestCase, mock

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.predictionWindow import *

app = QApplication(sys.argv)

class TestPredictionWindow(TestCase):
    # SET UP:
    def setUp(self):
        m = mock.Mock()
        self.test_window = PredictionWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Run predictions"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(600, 700))

    def test_import_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.get_import') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            importButton = test_window.import_button
            QTest.mouseClick(importButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_load_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.load_model') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            loadButton = test_window.load_model_button
            QTest.mouseClick(loadButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_default_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.load_default_model') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            defaultButton = test_window.load_default_model_button
            QTest.mouseClick(defaultButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_save_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.save_results') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            saveButton = test_window.save_button
            QTest.mouseClick(saveButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            homeButton = test_window.home_button
            QTest.mouseClick(homeButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_update_input_and_labels(self):
        self.fail()

    def test_get_seal_tag_popup(self):
        self.fail()

    def test_reset_input_fields_text(self):
        self.fail()

    def test_load_default_model_with_new_msg(self):
        self.fail()

    def test_clear_input_fields(self):
        self.fail()

    def test_update_feature_list(self):
        self.fail()

    def test_save_results(self):
        self.fail()

    def test_save_prediction(self):
        self.fail()

    def test_load_default_model(self):
        self.fail()

    def test_load_model(self):
        self.fail()

    def test_get_import(self):
        self.fail()

    def test_get_seal_tag(self):
        self.fail()

    def test_get_manual_input_prediction(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()