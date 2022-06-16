import sys
import unittest
from unittest import TestCase, mock

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.predictionWindow import PredictionWindow

########################################################################################################################
# File for testing the prediction window
########################################################################################################################


app = QApplication(sys.argv)


defaultFeatureList = ["WBC", "LYMF", "GRAN", "MID", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]

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
            import_button = test_window.import_button
            QTest.mouseClick(import_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_load_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.load_model') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            load_button = test_window.load_model_button
            QTest.mouseClick(load_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_default_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.load_default_model') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            default_button = test_window.load_default_model_button
            QTest.mouseClick(default_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_save_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.save_results') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            save_button = test_window.save_button
            QTest.mouseClick(save_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.predictionWindow.PredictionWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = PredictionWindow(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    # Update features without wbc should be disabled, check they are not enabled
    def test_update_input_and_labels(self):
        self.test_window.featureList = ["WBC"]
        self.test_window.update_input_and_labels()

        disable_input_list = [self.test_window.lymf_input, self.test_window.gran_input, self.test_window.mid_input, self.test_window.rbc_input,
                              self.test_window.hgb_input, self.test_window.mch_input, self.test_window.mchc_input, self.test_window.mpv_input, self.test_window.plt_input]

        self.assertTrue(self.test_window.wbc_input.isEnabled())

        for i in disable_input_list:
            self.assertFalse(i.isEnabled())

    # Check all feature inputs should be empty.
    def test_reset_input_fields_text(self):
        for input in self.test_window.featureInputDict.values():
            self.assertEqual("", input.text())

    @mock.patch("joblib.load")
    @mock.patch("GUI.predictionWindow.pop_message_box")
    def test_load_default_model_with_new_msg(self, mock_load, mock_pop):
        self.test_window.load_default_model_with_new_msg()

        defaultFeatureList = ["WBC", "LYMF", "GRAN", "MID", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]

        self.assertEqual("defaultModel", self.test_window.modelName)
        self.assertEqual(defaultFeatureList, self.test_window.featureList)
        mock_load.assert_called_once()
        mock_pop.assert_called_once()

    def test_update_feature_list(self):
        pass

    def test_save_results(self):
        pass

    def test_save_prediction(self):
        pass

    @mock.patch("joblib.load")
    @mock.patch("GUI.predictionWindow.pop_message_box")
    def test_load_default_model(self, mock_load, mock_pop):
        self.test_window.load_default_model()

        defaultFeatureList = ["WBC", "LYMF", "GRAN", "MID", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]

        self.assertEqual("defaultModel", self.test_window.modelName)
        self.assertEqual(defaultFeatureList, self.test_window.featureList)
        mock_load.assert_called_once()
        mock_pop.assert_called_once()

    # @mock.patch("joblib.load")
    # @mock.patch("GUI.predictionWindow.pop_message_box")
    # def test_load_model_success(self, mock_load, mock_update):
    #     with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName') as mock_qDialog:
    #         mock_qDialog.getOpenFileName(filter='PKL files (*.pkl)')[0].return_value = 'Tests/Test.pkl'
    #         result = self.test_window.load_model()
    #
    #         self.assertTrue(result)
    #         defaultFeatureList = ["WBC", "LYMF", "GRAN", "MID", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]
    #
    #         # self.assertEqual("Test", self.test_window.modelName)
    #         self.assertEqual(defaultFeatureList, self.test_window.featureList)
    #         mock_load.assert_called_once()
    #         mock_update.assert_called_once()
    #
    #
    #
    # @mock.patch("joblib.load")
    # @mock.patch("GUI.predictionWindow.pop_message_box")
    # def test_load_model_fail(self, mock_load, mock_pop):
    #     with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName') as mock_qDialog:
    #         mock_qDialog.getOpenFileName(filter='PKL files (*.pkl)')[0].return_value = ""
    #         result = self.test_window.load_model()
    #         print(result)
    #         self.assertFalse(result)

    def test_get_import(self):
        pass

    def test_get_seal_tag(self):
        pass

    def test_get_manual_input_prediction(self):
        pass

    def test_get_manual_input_prediction(self):
        self.test_window.combo1.addItem("Female")
        self.test_window.seal_tag_input.setText("Julia")

        self.test_window.featureList=defaultFeatureList
        self.test_window.wbc_input.setText("1")
        self.test_window.lymf_input.setText("2")
        self.test_window.gran_input.setText("3")
        self.test_window.mid_input.setText("4")
        self.test_window.rbc_input.setText("5")
        self.test_window.hgb_input.setText("6")
        self.test_window.mch_input.setText("7")
        self.test_window.mchc_input.setText("8")
        self.test_window.mpv_input.setText("9")
        self.test_window.plt_input.setText("10")

        self.test_window.featureInputDict = dict(zip(defaultFeatureList,self.test_window.default_input_list))
        output = ['Julia', 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 0, 0]

        self.test_window.get_manual_input_prediction()

        self.assertEqual(output,self.test_window.sealDataManualInput)


if __name__ == '__main__':
    unittest.main()
