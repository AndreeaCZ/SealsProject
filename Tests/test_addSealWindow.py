import os
import sys
import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
from GUI.addSealWindow import AddSealWindow
from variables import ROOT_DIR

########################################################################################################################
# File for testing the add seal window
########################################################################################################################

app = QApplication(sys.argv)


class TestAddSealWindow(TestCase):
    # SET UP:
    # Opening dummyDB for testing is not implemented yet.
    # If dummbyDB executed, all data in dummbyDB will be deleted and the DB will be closed when the tests ended.
    def setUp(self):
        m = mock.Mock()
        self.test_window = AddSealWindow(m)

    # Test Initial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), "Add a seal")

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

    # 1. test unique sealTag with excel file
    @mock.patch("GUI.addSealWindow.pop_message_box")
    @mock.patch("sqlite3.connect")
    def test_add_database_sucessfully(self, mock_pop, mock_db):
        test_file = os.path.join(ROOT_DIR, 'Tests/correct_testing_data.xlsx')
        test_tag = "test-1"

        result = self.test_window.add_to_database(test_file, test_tag)
        mock_db.return_value = mock.Mock()

        self.assertTrue(result)
        mock_pop.assert_called_once()
        mock_db.assert_called_once()

    # 2. test adding to database with wrong excel file
    @mock.patch("Utilities.excelManipulation.error_message_popup")
    def test_add_database_fail(self, mock_pop):
        test_file = os.path.join(ROOT_DIR, 'Tests/wrong_testing_data.xlsx')
        test_tag = "test-1"

        result = self.test_window.add_to_database(test_file, test_tag)

        self.assertFalse(result)
        mock_pop.assert_called_once()

    # 3. test add data with empty tagID
    @mock.patch("GUI.addSealWindow.pop_message_box")
    def test_empty_tagID(self, mock_pop):
        self.test_window.sealTag_input_line.setText("")
        result = self.test_window.add_seal()
        self.assertFalse(result)
        mock_pop.assert_called_once()


if __name__ == '__main__':
    unittest.main()
