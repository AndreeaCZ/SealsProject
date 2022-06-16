from sqlite3 import connect

import pandas as pd
import seaborn as sns

from variables import DB_PATH

########################################################################################################################
# This can be connected and used in the GUI to visualize the data.
########################################################################################################################


def data_visualization():
    conn = connect(DB_PATH)  # create a connection to the database
    # database connection
    dataset_labeled_seals = pd.read_sql('SELECT *  FROM sealPredictionData', conn)  # import data into dataframe
    dataset_labeled_seals = dataset_labeled_seals.drop(['sealTag'], axis=1)  # drop tag column
    g = sns.pairplot(dataset_labeled_seals, hue='Survival', vars=['WBC', 'LYMF', 'HCT', 'MCV', 'RBC', 'HGB', 'MCH', 'MCHC'
        , 'MPV', 'PLT'])
    g.savefig('dataVisulization.png')  # save plot

