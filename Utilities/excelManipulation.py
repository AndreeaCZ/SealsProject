import math

import numpy as np
from PyQt6.QtWidgets import QMessageBox

########################################################################################################################
# Contains usefule functions for the manipulation of Excel files
########################################################################################################################
from GUI.utils import pop_message_box


def get_blood_test_values(nparray, labels):
    # Get the values from the Excel file in numpy array format
    # Input: nparray, labels
    # Output: list of values
    values = []
    if not (low_in_array(nparray)):
        col_number = np.where(nparray == "LOW")[1][0]
        # labels with wrong input type
        wrong_labels = []
        for label in labels:
            if not (label_in_array(nparray, label)):
                e = nparray[np.where(nparray == label)[0][0]][col_number]
                if (isinstance(e, float) and not math.isnan(e)) or isinstance(e, int):
                    values.append(e)
                else:
                    wrong_labels.append(label)
            else:
                pop_message_box("Check that the correct file is being uploaded and contains a seal tag")
                return 0
        if is_empty(wrong_labels):
            return values
        # pops a message box if the input of the parameters is not a float or an integer
        else:
            error_message_popup(wrong_labels)
            return 0
    else:
        return 0


def label_in_array(nparray, label):
    return np.where(nparray == label)[0].size == 0


def low_in_array(nparray):
    return np.where(nparray == "LOW")[0].size == 0


def is_numeric(e):
    return (isinstance(e, float) and not math.isnan(e)) or isinstance(e, int)


def is_empty(nparray):
    return len(nparray) == 0


def error_message_popup(wrong_labels):
    msg_box = QMessageBox()
    msg_box.setText("These parameters have non-numeric input. Change it!" + str(wrong_labels))
    msg_box.exec()

