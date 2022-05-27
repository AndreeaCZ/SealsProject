from sqlite3 import connect
import pandas as pd
from variables import DB_PATH


def get_model_data():
    """
    Used to balance the data for the model to be trained on
    :return: balanced data
    """
    conn = connect(DB_PATH)
    sql_query = pd.read_sql_query('SELECT *  FROM sealPredictionData', conn)
    sealDataframe = pd.DataFrame(sql_query, columns=['WBC', 'LYMF', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT',
                                                     'Survival', 'Sex', 'Species'])
    survivalData = sealDataframe[sealDataframe['Survival'] == 1]
    deceasedData = sealDataframe[sealDataframe['Survival'] == 0]
    deceasedNumber = len(deceasedData)
    filteredSurvivalData = survivalData.sample(deceasedNumber)
    undersampledData = pd.concat([filteredSurvivalData, deceasedData], axis=0)

    return undersampledData
