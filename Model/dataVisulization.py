########################################################################################################################
# This can be connected and used in the GUI to visualize the data.
########################################################################################################################
import seaborn as sns
import pandas as pd
from sqlite3 import connect

from variables import DB_PATH

conn = connect(DB_PATH)  # create
# database connection
datasetLabeledSeals = pd.read_sql('SELECT *  FROM sealPredictionData', conn)  # import data into dataframe
datasetLabeledSeals = datasetLabeledSeals.drop(['sealTag', 'HCT', 'MCV'], axis=1)  # drop tag column

g = sns.pairplot(datasetLabeledSeals, hue='Survival', vars=['WBC', 'LYMF', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT'])
g.savefig('dataVisulization.png')  # save plot

