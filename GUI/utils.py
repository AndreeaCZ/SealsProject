import joblib
import numpy as np
import pandas as pd

from Utilities.excelManipulation import get_blood_test_values

# Makes the prediction and returns an array of values if input validation succeeds
# If not, it returns 0
def make_prediction(file_path, sex, species, model):
    new_seal_data = pd.read_excel(file_path).to_numpy()
    blood_results = get_blood_test_values(new_seal_data, ["WBC", "LYMF", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"])
    if not (blood_results == 0):
        blood_results = np.append(blood_results, [sex] + [species])
        return find_prediction(blood_results, model)
    else:
        return 0


def find_prediction(data, model):
    predictionArr = np.array(data).reshape(1, -1)
    compare = int(model.predict(predictionArr))
    output = "Values you entered:\n" + ", ".join(map(str, data)) + "\n\nModel prediction:\n"
    if compare == 1:
        return output + "Will survive"
    else:
        return output + "Will not survive"
