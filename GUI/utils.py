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


def make_prediction(file_path, sex, species, model, featureList):
    """
    Makes the prediction and returns an array of values if input validation succeeds.
    If not, it returns 0.
    :param file_path: path for getting input values
    :param sex: sex of the seal
    :param species: species of the seal
    :param model: model to be used for prediction
    :param featureList: features to be used for prediction
    :return: prediction string ready for output, blood values of the seal
    """
    new_seal_data = pd.read_excel(file_path).to_numpy()
    blood_results = get_blood_test_values(new_seal_data, featureList)
    if not (blood_results == 0):
        resultStr, survival = find_prediction(blood_results, model, sex, species)
        blood_results = np.append(blood_results, [sex] + [species] + [survival])
        return resultStr, blood_results
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
    predictionArr = np.append(data, [sex] + [species])
    predictionArr = np.array(predictionArr).reshape(1, -1)
    sexString = get_sex_str_from_int(sex)
    speciesString = get_seal_species_str_from_int(species)
    compare = int(model.predict(predictionArr))
    output = "Values you entered:\n" + ", ".join(map(str, data)) + ", " + sexString + ", " + speciesString + "\n\nModel prediction:\n"
    if compare == 1:
        return output + "Will survive", 1
    else:
        return output + "Will not survive", 0


# pops open a message box with the passed str as the message
def pop_message_box(string):
    msgBox = QMessageBox()
    msgBox.setText(string)
    msgBox.exec()


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
