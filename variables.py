import os

import joblib

DB_NAME = 'sealPredictionData.db'
DIV = '/'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'Database/sealPredictionData.db')
MODEL_PATH = os.path.join(ROOT_DIR, 'Model/RBDecisionTree.pkl')
ARRIVED_SEALS_PATH = os.path.join(ROOT_DIR, 'Arrived_seals_2014-2021.xlsx')
CLIENT_DATA_PATH = os.path.join(ROOT_DIR, 'clientData') # path to client data folder
#MODEL = joblib.load(MODEL_PATH)
