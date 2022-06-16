from sqlite3 import connect

import pandas as pd

from variables import DB_PATH

# ########################################################################################################################
# File used to retrieve all data present in the database
# ########################################################################################################################

def get_model_data():
    """
    Used to retrieve and balance the data from the database
    :return: balanced data
    """
    conn = connect(DB_PATH)
    sql_query = pd.read_sql_query('SELECT *  FROM sealPredictionData where Species = 0', conn)
    seal_dataframe = pd.DataFrame(sql_query, columns=['WBC', 'LYMF', 'GRAN', 'MID', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT',
                                                     'Survival', 'Sex', 'Species'])
    survival_data = seal_dataframe[seal_dataframe['Survival'] == 1]
    deceased_data = seal_dataframe[seal_dataframe['Survival'] == 0]
    deceased_number = len(deceased_data)
    filtered_survival_data = survival_data.sample(deceased_number)
    undersampled_data = pd.concat([filtered_survival_data, deceased_data], axis=0)

    return undersampled_data
