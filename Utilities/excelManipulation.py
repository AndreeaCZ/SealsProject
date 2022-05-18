import numpy as np
from PyQt6.QtWidgets import QMessageBox


def get_blood_test_values(nparray, labels):
    # Get the values from the excel file in numpy array format
    # Input: nparray, labels
    # Output: list of values
    values = []
    colNumber = np.where(nparray == "LOW")[1][0]
    # labels with wrong input type
    wrongLabels = []
    for label in labels:
       if isinstance(nparray[np.where(nparray == label)[0][0]][colNumber], float) or isinstance(nparray[np.where(nparray == label)[0][0]][colNumber], int):
            values.append(nparray[np.where(nparray == label)[0][0]][colNumber])
       else:
           wrongLabels.append(label)

    if (len(wrongLabels) == 0):
        return values
    # pops a message box if the input of the parameters is not a float or an integer
    else:
        msgBox = QMessageBox()
        msgBox.setText("These parameters have non-numeric input. Change it!" + str(wrongLabels))
        msgBox.exec()
        return 0
