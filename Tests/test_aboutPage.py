import sys
import unittest
from unittest import TestCase
from unittest import TestCase, mock
from unittest.mock import patch

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from PyQt6.QtWidgets import QApplication

from GUI.aboutPage import *

app = QApplication(sys.argv)


class test_about(TestCase):
    def setUp(self):
        m = mock.Mock()
        self.test_window = About(m)

    def test_title(self):
        self.assertEqual(self.test_window.windowTitle(), ("About"))

    def test_size(self):
        self.assertEqual(self.test_window.size(), QSize(800, 500))

    def test_button_clicked(self):
        with mock.patch('GUI.aboutPage.About.go_to_home') as clickCheck:
            m = mock.Mock()
            test_window = About(m)
            home_button = test_window.home_button
            QTest.mouseClick(home_button, Qt.MouseButton.LeftButton)
            self.assertTrue(clickCheck.called)


if __name__ == '__main__':
    unittest.main()
