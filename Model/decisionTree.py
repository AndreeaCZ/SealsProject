import joblib
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
from sqlite3 import connect
from sklearn import tree
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from variables import DB_PATH, MODEL_PATH

conn = connect(DB_PATH)

#######################################################################################################################
# Balancing the data


# retrive all the data from the database
sql_query = pd.read_sql_query('SELECT *  FROM sealPredictionData', conn)
# Create dataframe from the retrieved data. Note that we only want certain information to be included.
sealDataframe = pd.DataFrame(sql_query, columns=['WBC', 'LYMF', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT', 'Survival'])
# Create two different dataframe where one contains the filtered data for the survived seals
# and the other dataframe contain details about the dead seals
survivalData = sealDataframe[sealDataframe['Survival'] == 1]
unsurvivalData = sealDataframe[sealDataframe['Survival'] == 0]
# The amount of dead seals
unsurviveNumber = len(unsurvivalData)
# create another dataframe that contains the information about alive seals.
# Moreover the number of data is the same as the number of dead seals data
filteredSurvivalData = survivalData.sample(unsurviveNumber)
# Concatenate two dataframe, that is, the dataframe named 'filteredSurvivalData' is concatenated with
# the dataframe called 'unsurvivalData'
undersampledData = pd.concat([filteredSurvivalData, unsurvivalData], axis=0)

#######################################################################################################################
# Split the data into training set and testing set. Those training set is used to train the decision tree model


survivalDecisionTree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_leaf=6)
# separate features from labels
X = undersampledData.drop(['Survival'], axis=1)
scaler = MinMaxScaler()
# normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
X = scaler.fit_transform(X)
# get all labels
y = undersampledData['Survival'].values
# Split the data into training anf testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# Train the decision tree model
survivalDecisionTree = survivalDecisionTree.fit(X_train, y_train)
# Make the prediction with the testing set
predictions = survivalDecisionTree.predict(X_test)
# Evaluate the accuracy of the prediction
print(accuracy_score(y_test, predictions))

########################################################################################################################
# Data Visualization, Decision Tree - Graphical Representation, Confusion Matrix, Feature Importance


# Confusion Matrix
titles_options = [
    ("Confusion matrix, without normalization", None),
    ("Normalized confusion matrix", "true"),
]
for title, normalize in titles_options:
    disp = ConfusionMatrixDisplay.from_estimator(
        survivalDecisionTree,
        X_test,
        y_test,
        cmap=plt.cm.inferno,
        normalize=normalize
    )
    disp.ax_.set_title(title)

# print(title)
print(disp.confusion_matrix)

plt.show()

# Decision Tree - Graphical Representation
fig = plt.figure(figsize=(20, 20))
tree.plot_tree(survivalDecisionTree, filled=True, feature_names=undersampledData.drop(['Survival'], axis=1).columns,
               class_names=undersampledData['Survival'].unique().astype(str), rounded=True)
fig.show()

# Feature Importance
for i, column in enumerate(undersampledData.drop(['Survival'], axis=1).columns):
   print(column, ':', survivalDecisionTree.feature_importances_[i])

########################################################################################################################
# Export the model


joblib.dump(survivalDecisionTree, MODEL_PATH)