import numpy as np


def get_blood_test_values(nparray, labels):
    # Get the values from the excel file in numpy array format
    # Input: nparray, labels
    # Output: list of values
    values = []
    colNumber = np.where(nparray == "LOW")[1][0]
    for label in labels:
        values.append(nparray[np.where(nparray == label)[0][0]][colNumber])
    return values
