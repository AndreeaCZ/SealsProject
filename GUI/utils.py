import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QMessageBox

from Utilities.excelManipulation import get_blood_test_values

########################################################################################################################
# File contains useful functions and constants used by the GUI
########################################################################################################################


# Color constants
darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'


def make_prediction(file_path, sex, species, model, feature_list):
    """
    Makes the prediction and returns an array of values if input validation succeeds.
    If not, it returns 0.
    :param file_path: path for getting input values
    :param sex: sex of the seal
    :param species: species of the seal
    :param model: model to be used for prediction
    :param feature_list: features to be used for prediction
    :return: prediction string ready for output, blood values of the seal
    """
    new_seal_data = pd.read_excel(file_path).to_numpy()
    blood_results = get_blood_test_values(new_seal_data, feature_list)
    if blood_results != 0:
        result_str, survival = find_prediction(blood_results, model, sex, species)
        blood_results = np.append(blood_results, [sex] + [species] + [survival])
        return result_str, blood_results
    else:
        return 0, []


def find_prediction(data, model, sex, species):
    """
    Takes the data and uses the model to predict the seal's survival
    :param data: input data
    :param model: model to be used
    :param sex: sex of the seal
    :param species: species of the seal
    :return: result string ready for output
    """
    prediction_arr = np.append(data, [sex] + [species])
    prediction_arr = np.array(prediction_arr).reshape(1, -1)
    sex_string = get_sex_str_from_int(sex)
    species_string = get_seal_species_str_from_int(species)
    compare = int(model.predict(prediction_arr))
    output = "Values you entered:\n" + ", ".join(map(str, data)) + ", " + sex_string + ", " + species_string + "\n\nModel prediction:\n"
    if compare == 1:
        return output + "Will survive", 1
    else:
        return output + "Will not survive", 0


# pops open a message box with the passed str as the message
def pop_message_box(string):
    msg_box = QMessageBox()
    msg_box.setText(string)
    msg_box.exec()


# returns the species from the integer representation
def get_seal_species_str_from_int(x):
    if x == 0 or x == '0':
        return "Phoca Vitulina"
    if x == 1 or x == '1':
        return "Halichoerus Grypus"


# returns the sex from the integer representation
def get_sex_str_from_int(x):
    if x == 0:
        return "Female"
    if x == 1:
        return "Male"


# returns the survival from the integer representation
def get_chances_str_from_int(x):
    if x == 0:
        return "Will not survive"
    if x == 1:
        return "Will survive"


def get_seal_species_int(string):
    if string == "Phoca Vitulina":
        return 0
    if string == "Halichoerus Grypus":
        return 1


def get_sex_int(string):
    if string == "Female":
        return 0
    if string == "Male":
        return 1


def get_survival_str_from_int(x):
    if x == 0:
        return "Not released"
    if x == 1:
        return "Released"
