import sys
from unittest import TestCase, mock
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.queryDatabaseWindow import *

app = QApplication(sys.argv)

class TestQueryDatabaseWindow(TestCase):
    # SET UP:
    def setUp(self):
        m = mock.Mock()
        self.test_window = QueryDatabaseWindow(m)

    # TestInitial: title, size , button clicked working?
    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("Get seal data"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(700, 500))

    def test_home_button_clicked(self):
        with mock.patch('GUI.queryDatabaseWindow.QueryDatabaseWindow.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = QueryDatabaseWindow(m)
            homeButton = test_window.home_button
            QTest.mouseClick(homeButton, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)

    def test_get_min_tag_for_year(self):
        self.fail()

    def test_get_max_tag_for_year(self):
        self.fail()

    def test_get_excluded_value(self):
        self.fail()

    def test_get_year(self):
        self.fail()

    def test_save_data(self):
        self.fail()

    def test_execute_query(self):
        self.fail()

    def test_update_dataframe(self):
        self.fail()

    def test_set_default_values(self):
        self.fail()

    def test_set_elements(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()
