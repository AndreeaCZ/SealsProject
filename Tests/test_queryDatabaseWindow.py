import sys
import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.queryDatabaseWindow import QueryDatabaseWindow

########################################################################################################################
# File for testing the queryDatabaseWindow.py file.
########################################################################################################################


app = QApplication(sys.argv)


class TestQueryDatabaseWindow(TestCase):
    # SET UP:
    def setUp(self):
        m = mock.Mock()
        self.test_window = QueryDatabaseWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Query the database"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(900, 600))

    def test_home_button_clicked(self):
        with mock.patch('GUI.queryDatabaseWindow.QueryDatabaseWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = QueryDatabaseWindow(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_get_min_tag_for_year(self):
        result = self.test_window.get_min_tag_for_year(2014)
        self.assertEqual("T14-000", result)

    def test_get_max_tag_for_year(self):
        result = self.test_window.get_max_tag_for_year(2014)
        self.assertEqual("T14-999", result)

    def test_get_year(self):
        self.test_window.minYear.setText("2017")
        self.test_window.maxYear.setText("2020")
        result = self.test_window.get_year()
        self.assertEqual(('T17-000', 'T20-999'), result)

    @mock.patch("GUI.queryDatabaseWindow.pop_message_box")
    def test_execute_query(self, mock_pop):
        list_self_min = [self.test_window.minWBC, self.test_window.minLYMF, self.test_window.minGRAN,
                         self.test_window.minMID, self.test_window.minHCT, self.test_window.minMCV,
                         self.test_window.minRBC,
                         self.test_window.minHGB, self.test_window.minMCH, self.test_window.minMCHC,
                         self.test_window.minMPV, self.test_window.minPLT]
        list_self_max = [self.test_window.maxWBC, self.test_window.maxLYMF, self.test_window.maxGRAN,
                         self.test_window.maxMID, self.test_window.maxHCT, self.test_window.maxMCV,
                         self.test_window.maxRBC,
                         self.test_window.maxHGB, self.test_window.maxMCH, self.test_window.maxMCHC,
                         self.test_window.maxMPV, self.test_window.maxPLT]
        feature_list = ['WBC', 'LYMF', 'GRAN', 'MID', 'HCT', 'MCV', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT']
        for i in range(len(feature_list)):
            list_self_min[i].setText("1")
            list_self_max[i].setText("10")

        with patch('GUI.queryDatabaseWindow.sqlite3') as mock_db:
            mock_db.connect().cursor().fetchall.return_value = mock.MagicMock()
            self.test_window.execute_query()
            self.assertEqual(1, mock_db.connect().cursor().fetchall.call_count)
            mock_pop.assert_called_once()

    def test_set_default_values(self):
        list_self_min = [self.test_window.minWBC, self.test_window.minLYMF, self.test_window.minGRAN,
                         self.test_window.minMID, self.test_window.minHCT, self.test_window.minMCV,
                         self.test_window.minRBC,
                         self.test_window.minHGB, self.test_window.minMCH, self.test_window.minMCHC,
                         self.test_window.minMPV, self.test_window.minPLT]
        list_self_max = [self.test_window.maxWBC, self.test_window.maxLYMF, self.test_window.maxGRAN,
                         self.test_window.maxMID, self.test_window.maxHCT, self.test_window.maxMCV,
                         self.test_window.maxRBC,
                         self.test_window.maxHGB, self.test_window.maxMCH, self.test_window.maxMCHC,
                         self.test_window.maxMPV, self.test_window.maxPLT]
        feature_list = ['WBC', 'LYMF', 'GRAN', 'MID', 'HCT', 'MCV', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT']
        for i in range(len(feature_list)):
            list_self_min[i].setText("")
            list_self_max[i].setText("")

        with patch('GUI.queryDatabaseWindow.sqlite3') as mock_db:
            mock_db.connect().cursor().fetchall.return_value = mock.MagicMock()
            self.test_window.set_default_values()
            self.assertEqual(24, mock_db.connect().cursor().fetchall.call_count)


if __name__ == '__main__':
    unittest.main()
