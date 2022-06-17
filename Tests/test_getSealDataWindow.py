import sys
import unittest
from unittest import TestCase, mock
from unittest.mock import patch
import numpy as np
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.getSealDataWindow import GetSealDataWindow

########################################################################################################################
# File for testing the get seal data window.
########################################################################################################################


app = QApplication(sys.argv)


class TestGetSealDataWindow(TestCase):
    test_data = ['test-1', '1', '1', '1', '1', '1', '1', '1',
                 '1', '1', '1', '1', '1', '1', '1', '1']

    # SET UP:
    def setUp(self):
        m = mock.Mock()
        self.test_window = GetSealDataWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), "Get seal data")

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(700, 500))

    def test_get_button_clicked(self):
        with mock.patch('GUI.getSealDataWindow.GetSealDataWindow.get_seal_data') as clickCheck:
            m = mock.Mock()
            test_window = GetSealDataWindow(m)
            get_button = test_window.getSealData_button
            QTest.mouseClick(get_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.getSealDataWindow.GetSealDataWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = GetSealDataWindow(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_show_seal_data(self):
        x = np.array(['test-1', '1', '1', '1', '1', '1', '1', '1',
                      '1', '1', '1', '1', '1', '1', '1', '1'], dtype=object)
        self.test_window.show_seal_data(x)
        output = "sealTag - test-1\nWBC - 1\nLYMF - 1\n" \
                 "GRAN - 1\nMID - 1\nHCT - 1\nMCV - 1\nRBC - 1\n" \
                 "HGB - 1\nMCH - 1\nMCHC - 1\nMPV - 1\nPLT - 1\n" \
                 "Survival - Released\nSex - Male\nSpecies - Halichoerus Grypus\n"
        self.assertEqual(self.test_window.output_label.text(), output)

    @mock.patch("GUI.getSealDataWindow.GetSealDataWindow.show_seal_data")
    def test_get_seal_data_success(self, mock_show):
        # if seal tag is found in the database
        self.test_window.sealTag_input_line.setText("test-1")
        self.assertEqual(0, mock_show.call_count)
        with patch('GUI.getSealDataWindow.sqlite3') as mock_db:
            mock_db.connect().cursor().fetchone.return_value = self.test_data
            result = self.test_window.get_seal_data()
            self.assertTrue((result == self.test_data).all)
            self.assertEqual(1, mock_show.call_count)
            self.assertEqual(1, mock_db.connect().cursor().fetchone.call_count)


if __name__ == '__main__':
    unittest.main()
