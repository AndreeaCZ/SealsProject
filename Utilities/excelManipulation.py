import math

import numpy as np
from PyQt6.QtWidgets import QMessageBox, QApplication


def get_blood_test_values(nparray, labels):
    # Get the values from the excel file in numpy array format
    # Input: nparray, labels
    # Output: list of values
    values = []
    if not (np.where(nparray == "LOW")[0].size == 0):
        colNumber = np.where(nparray == "LOW")[1][0]
        # labels with wrong input type
        wrongLabels = []
        for label in labels:
            if not (np.where(nparray == label)[0].size == 0):
                e = nparray[np.where(nparray == label)[0][0]][colNumber]
                if (isinstance(e, float) and not math.isnan(e)) or isinstance(e, int):
                    values.append(e)
                else:
                    wrongLabels.append(label)
            else:
                pop_message_box("Check that the correct file is being uploaded and contains a seal tag")
                return 0
        if (len(wrongLabels) == 0):
            return values
        # pops a message box if the input of the parameters is not a float or an integer
        else:
            error_message_popup(wrongLabels)
            return 0
    else:
        return 0


def error_message_popup(wrongLabels):
    msgBox = QMessageBox()
    msgBox.setText("These parameters have non-numeric input. Change it!" + str(wrongLabels))
    msgBox.exec()


# pops open a message box with the passed str as the message
def pop_message_box(string):
    msgBox = QMessageBox()
    msgBox.setText(string)
    msgBox.exec()
