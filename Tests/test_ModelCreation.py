
import unittest
import collections
import sys
import numpy
#numpy.set_printoptions(threshold=sys.maxsize)

from Model.modelCreation import *

collections.Callable = collections.abc.Callable

class test_data_visualization(unittest.TestCase):

    def test_data_preprocessing(self):
        x_train, x_test, y_train, y_test = data_preprocessing()

        # y_train and y_test should only hold value 1 or 0
        y=all((y_train==0)|(y_train==1))
        self.assertTrue(y)

        z = all((y_test == 0) | (y_test == 1))
        self.assertTrue(z)

        # X_train and X_test should only hold values between 1-0 #TODO: These fails sometimes
        x = ((x_train >= 0)&(x_train <= 1))
        self.assertNotIn(False,x)

        t = ((x_test >= 0) & (x_test <= 1))
        self.assertNotIn(False, t)

    def test_rf_Model(self):
        rf=rf_model()

        # Check the properties
        self.assertEqual(rf.max_depth,7)
        self.assertEqual(rf.min_samples_split,10)
        self.assertEqual(rf.random_state,42)
        self.assertEqual(rf.n_estimators,300)

        # Predictions should only hold values of 1 or 0
        x_train, x_test, y_train, y_test = data_preprocessing()
        rf = rf.fit(x_train, y_train)  # train the model
        predictions = rf.predict(x_test)  # make predictions on the test set
        y = all((predictions == 0) | (predictions == 1))
        self.assertTrue(y)


if __name__ == '__main__':
    unittest.main()




