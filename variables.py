import os

DB_NAME = 'sealPredictionData.db'
DIV = '/'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'sealPredictionData.db')
MODEL_PATH = os.path.join(ROOT_DIR, 'RFDecisionTree.pkl')
ABOUT_PATH = os.path.join(ROOT_DIR, 'about.txt')
DESCRIPTION_PATH = os.path.join(ROOT_DIR, 'description.txt')
ARRIVED_SEALS_PATH = os.path.join(ROOT_DIR, 'Arrived_seals_2014-2021.xlsx')
CLIENT_DATA_PATH = os.path.join(ROOT_DIR, 'clientData')
FEATURE_CHECKLIST_PATH = os.path.join(ROOT_DIR, 'featuresChecklist.xlsx')
