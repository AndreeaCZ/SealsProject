import numpy as np


def get_data(dataset, name, perc):
    rowNumber = 0
    colNumber = np.where(dataset == "LOW")[1][0]
    rows = np.where(dataset == name)[0]
    if perc:
        for i in rows:
            if dataset[i][1] == "%":
                rowNumber = i
                break
    else:
        for i in rows:
            if dataset[i][1] != "%":
                rowNumber = i
                break
    # print("success", rowNumber, colNumber)
    return dataset[rowNumber][colNumber]
