import joblib
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from Database.modelDataGeneration import get_model_data
from variables import MODEL_PATH


def data_preprocessing():
    """
    Data preprocessing for the model
    :return: the preprocessed data
    """
    data = get_model_data()
    X = data.drop(['Survival', 'Species', 'Sex'], axis=1)
    # separate features from labels

    scaler = MinMaxScaler()
    # normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
    X = scaler.fit_transform(X)
    y = data['Survival'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    return X_train, X_test, y_train, y_test


# feedForwardModel accuracy = 0.601
# highest accuracy = 0.602
def decisionTree():
    """
    Decision Tree model creation
    :return: the decision tree model
    """
    survivalDecisionTree = tree.DecisionTreeClassifier(criterion='entropy', min_samples_split=2)
    X_train, X_test, y_train, y_test = data_preprocessing()
    survivalDecisionTree = survivalDecisionTree.fit(X_train, y_train)
    return survivalDecisionTree


# highest accuracy = 0.65
def rf_Model():
    X_Train, X_Test, y_Train, y_Test = data_preprocessing()
    rf = RandomForestClassifier(criterion='entropy', n_estimators=300, max_depth=7, random_state=42, bootstrap=True,
                                max_features='auto', min_samples_leaf=1, min_samples_split=10)
    rf.fit(X_Train, y_Train)
    return rf


# highest accuracy = 0.64
def SVM():
    """
    SVM model creation
    :return: the SVM model
    """
    X_train, X_test, y_train, y_test = data_preprocessing()
    svmModel = svm.SVC(kernel='rbf', gamma='auto', C=9, probability=True, class_weight='balanced', max_iter=-1,
                       tol=1e-9)
    svmModel = svmModel.fit(X_train, y_train)
    return svmModel


# highest accuracy = 0.641
def KNeighbors():
    """
    KNeighbors model creation
    :return: the KNeighbors model
    """
    X_train, X_test, y_train, y_test = data_preprocessing()
    knnModel = KNeighborsClassifier(n_neighbors=5, algorithm='auto', weights='distance', n_jobs=-1)
    knnModel = knnModel.fit(X_train, y_train)
    return knnModel


# highest accuracy = 0.645, fluctuating a lot
def logisticRegression():
    """
    Logistic regression model creation
    :return: the logistic regression model
    """
    X_train, X_test, y_train, y_test = data_preprocessing()
    lr = LogisticRegression(C=7, solver='saga', multi_class='auto', max_iter=10000, tol=1e-3, warm_start=True,
                            n_jobs=-1)
    lr = lr.fit(X_train, y_train)
    return lr


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


def treePlotting(model):
    """
    Data visualization of the model
    :param model:
    :return:
    """
    data = get_model_data()
    fig = plt.figure(figsize=(20, 20))
    tree.plot_tree(model, filled=True, feature_names=data.drop(['Survival'], axis=1).columns,
                   class_names=data['Survival'].unique().astype(str), rounded=True)
    fig.savefig(MODEL_PATH + 'treePlot.png')
    fig.show()


def export_model(model):
    """
    Export the model
    :param model: the model to be exported
    :return: void function
    """
    # joblib.dump(model, MODEL_PATH + 'predictionModel.pkl')
    joblib.dump(model, MODEL_PATH)


########################################################################################################################
# Testing only
########################################################################################################################
def feature_importance(model):
    """
    Feature importance of the model
    :param model: model of which the features' importance is to be calculated
    :return:
    """
    data = get_model_data()
    for i, column in enumerate(data.drop(['Survival', 'Species', 'Sex'], axis=1).columns):
        print(column, ':', model.feature_importances_[i])


test_model = rf_Model()

feature_importance(test_model)
test_accuracy(test_model)
# perform feature selection
# drop the features that are not important: species, sex
# need to be tested: GRAN, MID
