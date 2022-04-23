import joblib
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
from sqlite3 import connect
from sklearn import tree
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


conn = connect(r'C:\Users\dobre\OneDrive\デスクトップ\Software Engineering\SealsProject\sealPredictionData.db')  # create
# database connection
datasetLabeledSeals = pd.read_sql('SELECT *  FROM sealPredictionData', conn)  # import data into dataframe
datasetLabeledSeals = datasetLabeledSeals.drop(['sealTag', 'HCT', 'MCV'], axis=1)  # drop tag column
# print(datasetLabeledSeals['Survival'].value_counts())  # check unbalanced data
survivalDecisionTree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_leaf=6)

X = datasetLabeledSeals.drop(['Survival'], axis=1)  # separate features from labels
scaler = MinMaxScaler()
X = scaler.fit_transform(X)  # normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
y = datasetLabeledSeals['Survival'].values  # get all labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)  # split data into training
# and test
survivalDecisionTree = survivalDecisionTree.fit(X_train, y_train)  # train the model
predictions = survivalDecisionTree.predict(X_test)  # make predictions on the test set
print(accuracy_score(y_test, predictions))  # evaluate accuracy

########################################################################################################################
# Data Visualization, Decision Tree - Graphical Representation, Confusion Matrix, Feature Importance

# Data Visualization
g = sns.pairplot(datasetLabeledSeals, hue='Survival', vars=['WBC', 'LYMF', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT'])
# shows distribution of variables in pairplot and shows the correlation between survival and the variables
# we can use this to see which variables have the most impact on survival, or which variables are irrelevant

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

    print(title)
    print(disp.confusion_matrix)

plt.show()

# Decision Tree - Graphical Representation
fig = plt.figure(figsize=(20, 20))
tree.plot_tree(survivalDecisionTree, filled=True, feature_names=datasetLabeledSeals.drop(['Survival'], axis=1).columns,
               class_names=datasetLabeledSeals['Survival'].unique().astype(str), rounded=True)
fig.show()

# Feature Importance
for i, column in enumerate(datasetLabeledSeals.drop(['Survival'], axis=1).columns):
    print(column, ':', survivalDecisionTree.feature_importances_[i])
########################################################################################################################

joblib.dump(survivalDecisionTree, 'SealDecisionTree.pkl')
