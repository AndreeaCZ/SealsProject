import joblib
import numpy as np

SealDecisionTree = joblib.load('SealDecisionTree.pkl')  # load the model created in the training phase
###################################### Replace the manual input with the dashboard input ###############################
wbc = input("Enter WBC: ")
lymph = input("Enter Lymph: ")
lymphPercent = input("Enter Lymph Percent: ")
# You can just copy this code into the dashboard file and connect the button to the .prediction function
# (with SealDecisionTree as the model)
########################################################################################################################
predictionArr = np.array([wbc, lymph, lymphPercent]).reshape(1, -1)
compare = int(SealDecisionTree.predict(predictionArr))
if compare == 1:
    print("Will survive")
else:
    print("Will not survive")
