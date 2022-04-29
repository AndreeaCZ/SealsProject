# possibly not needed anymore

import sqlite3

from SealsProject.variables import DB_NAME

connection = sqlite3.connect(DB_NAME)  # create a database for model training data
c = connection.cursor()
c.execute("")
c.execute('''
          CREATE TABLE IF NOT EXISTS sealPredictionData
          ([sealTag] TEXT PRIMARY KEY, [WBC] INTEGER NOT NULL, [LYMF] INTEGER NOT NULL, 
          [HCT] INTEGER NOT NULL, [MCV] INTEGER NOT NULL, [RBC] INTEGER NOT NULL, 
          [HGB] INTEGER NOT NULL, [MCH] INTEGER NOT NULL, [MCHC] INTEGER NOT NULL, [MPV] INTEGER NOT NULL,
          [PLT] INTEGER NOT NULL, [Survival] INTEGER NOT NULL)
          ''')
connection.commit()
connection.close()
