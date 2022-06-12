import sqlite3
import sys
import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.addSealWindow import *
from variables import DB_PATH

app = QApplication(sys.argv)

class TestAddSealWindow(TestCase):
    # SET UP:
    # Open window and attach bot to window
    def setUp(self):

        m = mock.Mock()
        self.test_window = AddSealWindow(m)
        # connection = sqlite3.connect("dummy_db")  # create a database for model training data
        # c = connection.cursor()
        # c.execute("")
        # c.execute('''
        #           CREATE TABLE IF NOT EXISTS sealPredictionData
        #           ([sealTag] TEXT PRIMARY KEY, [WBC] INTEGER NOT NULL, [LYMF] INTEGER NOT NULL,
        #            [HCT] INTEGER NOT NULL, [MCV] INTEGER NOT NULL, [RBC] INTEGER NOT NULL,
        #           [HGB] INTEGER NOT NULL, [MCH] INTEGER NOT NULL, [MCHC] INTEGER NOT NULL, [MPV] INTEGER NOT NULL,
        #           [PLT] INTEGER NOT NULL, [Survival] INTEGER NOT NULL, [Sex] INTEGER NOT NULL, [Species] INTEGER NOT NULL)
        #           ''')
        # connection.commit()
        # connection.close()

        # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Add a seal"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(700, 400))

    def test_add_button_clicked(self):
        with mock.patch('GUI.addSealWindow.AddSealWindow.add_seal') as clickCheck:
            m = mock.Mock()
            test_window = AddSealWindow(m)
            addButton = test_window.addSeal_button
            QTest.mouseClick(addButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_home_button_clicked(self):
        with mock.patch('GUI.addSealWindow.AddSealWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = AddSealWindow(m)
            homeButton = test_window.home_button
            QTest.mouseClick(homeButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_add_to_database_in_success(self):





# add Seal
    # if sealTag null
    #

    # add to database


    # test unique tagID

    #test same tagID
    # add database(file)
# class TestAdd(TestAddSealWindow):
#     def









    # def setUp(self):
    #     super(TestAddSealWindow, self).setUp()
    #     self.test_window = AddSealWindow()
    #     connection = sqlite3.connect("dummy_db")  # create a database for model training data
    #     c = connection.cursor()
    #     c.execute("")
    #     c.execute('''
    #               CREATE TABLE IF NOT EXISTS sealPredictionData
    #               ([sealTag] TEXT PRIMARY KEY, [WBC] INTEGER NOT NULL, [LYMF] INTEGER NOT NULL,
    #                [HCT] INTEGER NOT NULL, [MCV] INTEGER NOT NULL, [RBC] INTEGER NOT NULL,
    #               [HGB] INTEGER NOT NULL, [MCH] INTEGER NOT NULL, [MCHC] INTEGER NOT NULL, [MPV] INTEGER NOT NULL,
    #               [PLT] INTEGER NOT NULL, [Survival] INTEGER NOT NULL, [Sex] INTEGER NOT NULL, [Species] INTEGER NOT NULL)
    #               ''')
    #     connection.commit()
    #     connection.close()
    #
    # def tearDown(self):
    #     super(TestAddSealWindow, self).tearDown()
    #     pass
    #
    # def test_init_ok(self):
    #     self.assertEqual(self.test_window.windowTitle(), ("Add a seal"))
    #     # window size
    #     self.assertEqual(self.test_window.size(), Qt.QSize(700, 400))
    #
    # def test_add_seal_successful(self):
    #     self.test_window.sealTag_input_line.setText("2")
    #     self.test_window.add_seal()
    #
    #
    #     # check value in dummyDB
    #     sql = """SELECT * FROM dummy_db WHERE sealTag = 2"""
    #     c.execute(sql, (sealTag,))
    #     sealData = c.fetchone()
    #     npSealData = np.array(sealData)
    #     self.show_seal_data(npSealData)


    #
    # def test_add_seal_null(self):
    #     self.test_window = AddSealWindow()
    #     addWidget = self.test_window.addSeal_button
    #     qTest.mouseClick(addWidget, Qt.LeftButton)
    #     # testing null id
    #     pass
    #     self.fail()

        # testing import null path

        # testing import successful path

        # testing wrong path (wrong excel file)

        # testing null id

        # self.fail()
    #
    #
    # def test_add_seal(self):
    #     pass
    #
    # def test_add_to_database(self):
    #     # testing same id
    #
    #
    #     self.test_window.add_to_database(self, import_path, )
    #
    #     # testing unique id
    #     assert False
    #     self.fail()


if __name__ == '__main__':
    unittest.main()