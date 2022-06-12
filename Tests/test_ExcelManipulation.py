
import unittest
import collections

import numpy as np

from Utilities.excelManipulation import *

collections.Callable = collections.abc.Callable

class test_excel_manipulation(unittest.TestCase):

    def test_label_in_array(self):
        # Should return False if the label is in the array
        x = np.array([['a', 'LOW'], ['WBC', 8.6]], dtype=object)
        value = label_in_array(x, ["WBC"])
        self.assertEqual(value, False)

        # Should return True if the label is NOT in the array
        x = np.array([['a', 'LOW'], ['WBC', 8.6], ['LYMF', 59], ['GRAN', 3.16]], dtype=object)
        value = label_in_array(x, ["WC"])
        self.assertEqual(value, True)

    def test_low_in_array(self):
        # Should return False if "LOW" is in the array
        x = np.array([['a', 'LOW'], ['WBC', 8.6]], dtype=object)
        value = low_in_array(x)
        self.assertEqual(value, False)

        # Should return True if "LOW" is NOT in the array
        x = np.array([['a', 'LW'], ['WBC', 8.6]], dtype=object)
        value = low_in_array(x)
        self.assertEqual(value, True)

    def test_is_numeric(self):
        x=3
        y=0.5
        z='a'
        self.assertEqual(is_numeric(x), True)
        self.assertEqual(is_numeric(y), True)
        self.assertEqual(is_numeric(z), False)

    def test_is_empty(self):
        x=[]
        y=["XY"]
        self.assertEqual(is_empty(x), True)
        self.assertEqual(is_empty(y), False)

    def test_get_blood_test_values(self):
        #Checks that it gets correct value
        x = np.array([['a', 'LOW'], ['WBC', 8.6]],dtype=object)
        value = get_blood_test_values(x,["WBC"])
        self.assertEqual(value,[8.6])

        # Checks that it gets correct value, for multiple labels
        x = np.array([['a', 'LOW'], ['WBC', 8.6], ['LYMF', 59], ['GRAN', 3.16]], dtype=object)
        value = get_blood_test_values(x, ["WBC", "LYMF"])
        self.assertEqual(value, [8.6, 59])

        # Should return 0 when there is no "LOW" object
        x = np.array([['a', 'LO'], ['WBC', 8.6]], dtype=object)
        value = get_blood_test_values(x, ["WBC"])
        self.assertEqual(value, 0)


if __name__ == '__main__':
    unittest.main()


