import joblib
from matplotlib import pyplot as plt
from sklearn import tree
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from Database.modelDataGeneration import get_model_data
from variables import MODEL_PATH


def data_preprocessing():
    """
    Data preprocessing for the model
    :param data: the data to be preprocessed
    :return: the preprocessed data
    """
    data = get_model_data()
    X = data.drop(['Survival'], axis=1)
    # separate features from labels

    scaler = MinMaxScaler()
    # normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
    X = scaler.fit_transform(X)
    y = data['Survival'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test


def decisionTree():
    """
    Decision Tree model creation
    :return: the decision tree model
    """
    survivalDecisionTree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_leaf=5)
    X_train, X_test, y_train, y_test = data_preprocessing()
    survivalDecisionTree = survivalDecisionTree.fit(X_train, y_train)
    # Make the prediction with the testing set
    # Evaluate the accuracy of the prediction
    return survivalDecisionTree


def test_accuracy(model):
    """
    Test the accuracy of the model
    :param model: the model to be tested
    """
    X_train, X_test, y_train, y_test = data_preprocessing()
    predictions = model.predict(X_test)
    print("Accuracy: " + str(accuracy_score(y_test, predictions)))


def plot_confusion_matrix(model):
    """
    Plot the confusion matrix
    :param model: the model of which the confusion matrix is to be plotted
    """
    X_train, X_test, y_train, y_test = data_preprocessing()
    titles_options = [
        ("Confusion matrix, without normalization", None),
        ("Normalized confusion matrix", "true"),
    ]
    for title, normalize in titles_options:
        disp = ConfusionMatrixDisplay.from_estimator(
            model,
            X_test,
            y_test,
            cmap=plt.cm.inferno,
            normalize=normalize
        )
        disp.ax_.set_title(title)

    # print(title)
    print(disp.confusion_matrix)

    plt.show()


def data_visualization(model):
    data = get_model_data()
    fig = plt.figure(figsize=(20, 20))
    tree.plot_tree(model, filled=True, feature_names=data.drop(['Survival'], axis=1).columns,
                   class_names=data['Survival'].unique().astype(str), rounded=True)
    fig.show()


# Decision Tree - Graphical Representation


# Feature Importance
def feature_importance(model):
    data = get_model_data()
    for i, column in enumerate(data.drop(['Survival'], axis=1).columns):
        print(column, ':', model.feature_importances_[i])


########################################################################################################################
# Export the model

def export_model(model):
    joblib.dump(model, MODEL_PATH + 'predictionModel.pkl')
    joblib.dump(model, MODEL_PATH)
