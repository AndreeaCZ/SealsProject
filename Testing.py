import joblib
import numpy as np

SealDecisionTree = joblib.load('SealDecisionTree.pkl')  # load the model created in the training phase

wbc = input("Enter WBC: ")
lymph = input("Enter Lymph: ")
gran = input("Enter Gran: ")
mid = input("Enter Mid: ")
lymphPercent = input("Enter Lymph Percent: ")
granPercent = input("Enter Gran Percent: ")
midPercent = input("Enter Mid Percent: ")
hct = input("Enter Hct: ")
mcv = input("Enter Mcv: ")
rbc = input("Enter Rbc: ")
hgb = input("Enter Hgb: ")
mch = input("Enter Mch: ")
mchc = input("Enter Mchc: ")
plt = input("Enter Plt: ")

predictionArr = np.array([wbc, lymph, gran, mid, lymphPercent, granPercent, midPercent, hct, mcv, rbc, hgb, mch, mchc,
                          plt]).reshape(1, -1)
compare = int(SealDecisionTree.predict(predictionArr))
if compare == 1:
    print("Will survive")
else:
    print("Will not survive")


