########################################################################################################################
# This can be connected and used in the GUI to visualize the data.
########################################################################################################################
from sqlite3 import connect

import pandas as pd
import seaborn as sns

from variables import DB_PATH


def data_visualization():
    conn = connect(DB_PATH)  # create a connection to the database
    # database connection
    datasetLabeledSeals = pd.read_sql('SELECT *  FROM sealPredictionData', conn)  # import data into dataframe
    datasetLabeledSeals = datasetLabeledSeals.drop(['sealTag'], axis=1)  # drop tag column
    g = sns.pairplot(datasetLabeledSeals, hue='Survival', vars=['WBC', 'LYMF', 'HCT', 'MCV', 'RBC', 'HGB', 'MCH', 'MCHC'
        , 'MPV', 'PLT'])
    g.savefig('dataVisulization.png')  # save plot

