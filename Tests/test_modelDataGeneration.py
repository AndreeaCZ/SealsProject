
import unittest
import collections

import numpy as np

from Model.modelCreation import *

collections.Callable = collections.abc.Callable

class test_model_data_generation(unittest.TestCase):

    def test_label_in_array(self):
        # The amount of columns in database should be 13
        data=get_model_data()
        self.assertEqual(data.shape[1],13)

        # Prints database
        print(data)

        # Check that all column names are correct
        x=['WBC' in data, 'GRAN' in data, 'MID' in data, 'RBC' in data, 'LYMF' in data,
           'HGB' in data, 'MCH' in data, 'MCHC' in data, 'MPV' in data, 'PLT' in data, 'Survival' in data, 'Sex' in data, 'Species' in data]
        x=all(x)
        self.assertTrue(x)

        # Survival column should only hold values of 0 or 1
        survival_data = data['Survival']
        y = all(( survival_data == 0) | (survival_data == 1))
        self.assertTrue(y)

        # Sex column should only hold values of 0 or 1
        sex_data = data['Sex']
        y = all((sex_data == 0) | (sex_data == 1))
        self.assertTrue(y)

        # Species column should only hold values of 0
        species_data = data['Species']
        y = all((species_data == 0))
        self.assertTrue(y)


if __name__ == '__main__':
    unittest.main()


