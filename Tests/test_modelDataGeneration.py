
import unittest
import collections

import numpy as np

from Model.modelCreation_Testing import *

collections.Callable = collections.abc.Callable

class testModelDataGeneration(unittest.TestCase):

    #TODO: Add more tests here
    def test_label_in_array(self):
        # The amount of entries in database should be 628
        data=get_model_data()
        print(data)
        self.assertEqual(len(data), 628)

        # Amount of surviving seals should be 314
        survivalData = data[data['Survival'] == 1]
        self.assertEqual(len(survivalData), 314)

if __name__ == '__main__':
    unittest.main()


