
import unittest
import collections

import numpy as np

from Model.modelCreation_Testing import *

collections.Callable = collections.abc.Callable

class testModelDataGeneration(unittest.TestCase):

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
        survivalData = data['Survival']
        y = all(( survivalData == 0) | (survivalData == 1))
        self.assertTrue(y)

        # Sex column should only hold values of 0 or 1
        sexData = data['Sex']
        y = all((sexData == 0) | (sexData == 1))
        self.assertTrue(y)

        # Species column should only hold values of 0
        speciesData = data['Species']
        y = all((speciesData == 0))
        self.assertTrue(y)


if __name__ == '__main__':
    unittest.main()


