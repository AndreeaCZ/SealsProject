import joblib
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from Database.modelDataGeneration import get_model_data
from variables import MODEL_PATH


def data_preprocessing(data):
    """
    Data preprocessing for the model
    :return: the preprocessed data
    """
    X = data.drop(['Survival'], axis=1)
    # separate features from labels

    scaler = MinMaxScaler()
    # normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
    X = scaler.fit_transform(X)
    y = data['Survival'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    return X_train, X_test, y_train, y_test


# feedForwardModel accuracy = 0.601
# decision tree highest accuracy = 0.602
# highest accuracy = 0.65
# svm highest accuracy = 0.64
# kneighbours highest accuracy = 0.641
# logRegression highest accuracy = 0.645, fluctuating a lot

def rf_Model():
    rf = RandomForestClassifier(criterion='entropy', n_estimators=300, max_depth=7, random_state=42, bootstrap=True,
                                max_features='auto', min_samples_leaf=1, min_samples_split=10)

    return rf


def test_accuracy(model, X_test, y_test):
    """
    Test the accuracy of the model
    :param model: the model to be tested
    """
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)


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


# def treePlotting(model):
#     """
#     Data visualization of the model
#     :param model:
#     :return:
#     """
#     data = get_model_data()
#     fig = plt.figure(figsize=(20, 20))
#     tree.plot_tree(model, filled=True, feature_names=data.drop(['Survival'], axis=1).columns,
#                    class_names=data['Survival'].unique().astype(str), rounded=True)
#     fig.savefig(MODEL_PATH + 'treePlot.png')
#     fig.show()


def export_model(model):
    """
    Export the model
    :param model: the model to be exported
    :return: void function
    """
    joblib.dump(model, MODEL_PATH)


def feature_importance(model):
    """
    Feature importance of the model
    :param model: model of which the features' importance is to be calculated
    :return:
    """
    data = get_model_data()
    for i, column in enumerate(data.drop(['Survival'], axis=1).columns):
        print(column, ':', model.feature_importances_[i])

# perform feature selection
# drop the features that are not important: species, sex
# need to be tested: GRAN, MID
