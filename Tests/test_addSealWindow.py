import sys
import unittest
from unittest import TestCase, mock

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.addSealWindow import AddSealWindow

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
    # NOT IMPLEMENTED YET
    def test_add_database_sucessfully(self):
        self.test_window.import_path = 'Tests/correct_testing_data.xlsx'
        self.test_window.sealTag_input_line.setText("3")
        self.fail()

    # 2. test duplicated sealTag with excel file
    # NOT IMPLEMENTED YET
    def test_same_tagID(self):
        self.fail()

    # 3. test add data with empty tagID
    # NOT IMPLEMENTED YET
    def test_empty_tagID(self):
        self.fail()

    # 4. test wrong excel file
    # NOT IMPLEMENTED YET
    def test_add_with_wrong_excel_file(self):
        self.test_window.import_path = 'Tests/wrong_testing_data.xlsx'
        self.fail()


if __name__ == '__main__':
    unittest.main()
