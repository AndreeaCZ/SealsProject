import numpy as np
import pandas as pd

from Utilities.excelManipulation import get_blood_test_values
import numpy as np
import pandas as pd

from Utilities.excelManipulation import get_blood_test_values

# Color constants
darkblue = '#095056'
lightblue = '#669fa8'
darkorange = '#ff8a35'
lightorange = '#ffba87'
darkgray = '#3F4B5A'
lightgray = '#6A7683'


# Makes the prediction and returns an array of values if input validation succeeds
# If not, it returns 0
def make_prediction(file_path, sex, species, model, featureList):
    new_seal_data = pd.read_excel(file_path).to_numpy()
    blood_results = get_blood_test_values(new_seal_data, featureList)
    if not (blood_results == 0):
        resultStr, survival = find_prediction(blood_results, model, sex, species)
        blood_results = np.append(blood_results, [sex] + [species] + [survival])
        print(resultStr)
        return resultStr, blood_results
    else:
        return 0, []


def find_prediction(data, model, sex, species):
    predictionArr = np.append(data, [sex] + [species])
    predictionArr = np.array(predictionArr).reshape(1, -1)
    sexString = getSexStrFromInt(sex)
    speciesString = getSealSpeciesStrFromInt(species)
    compare = int(model.predict(predictionArr))
    output = "Values you entered:\n" + ", ".join(map(str, data)) + ", " + sexString + ", " + speciesString + "\n\nModel prediction:\n"
    if compare == 1:
        return output + "Will survive", 1
    else:
        return output + "Will not survive", 0

# returns the species from the integer representation
def getSealSpeciesStrFromInt(x):
    if x == 0:
        return "Phoca Vitulina"
    if x == 1:
        return "Halichoerus Grypus"

# returns the sex from the integer representation
def getSexStrFromInt(x):
    if x == 0:
        return "Female"
    if x == 1:
        return "Male"
