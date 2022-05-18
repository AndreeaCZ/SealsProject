import joblib
import numpy as np
import pandas as pd

from Utilities.excelManipulation import get_blood_test_values
from variables import MODEL_PATH

SealDecisionTree = joblib.load(MODEL_PATH)  # load the model created in the training phase

# Makes the prediction and returns an array of values if input validation succeeds
# If not, it returns 0
def make_prediction(file_path):
    new_seal_data = pd.read_excel(file_path).to_numpy()
    blood_results = get_blood_test_values(new_seal_data, ["WBC", "LYMF", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"])
    if not (blood_results == 0):
        blood_results = np.append(blood_results, [0,1,0,1])
        return find_prediction(blood_results)
    else:
        return 0


def find_prediction(data):
    predictionArr = np.array(data).reshape(1, -1)
    compare = int(SealDecisionTree.predict(predictionArr))
    output = "Values you entered:\n" + ", ".join(map(str, data)) + "\n\nModel prediction:\n"
    if compare == 1:
        return output + "Will survive"
    else:
        return output + "Will not survive"


