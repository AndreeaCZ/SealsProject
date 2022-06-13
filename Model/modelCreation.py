import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from Database.modelDataGeneration import get_model_data
from variables import MODEL_PATH


def data_preprocessing():
    """
    Data preprocessing for the model
    :return: the preprocessed data
    """
    data = get_model_data()
    X = data.drop(['Survival', 'Species'], axis=1)
    # separate features from labels

    scaler = MinMaxScaler()
    # normalize the data ( MinMaxScaler ) - scale the data to be between 0 and 1
    X = scaler.fit_transform(X)
    y = data['Survival'].values
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    return x_train, x_test, y_train, y_test


# feedForwardModel accuracy = 0.601
# highest accuracy = 0.602 Decision Tree
# highest accuracy = 0.65
def rf_model():
    rf = RandomForestClassifier(criterion='entropy', n_estimators=300, max_depth=7, random_state=42, bootstrap=True,
                                max_features='auto', min_samples_leaf=1, min_samples_split=10)
    return rf


# highest accuracy = 0.64 SVM
# highest accuracy = 0.641 KNN
# highest accuracy = 0.645, fluctuating a lot LR
def test_accuracy(model):
    """
    Test the accuracy of the model
    :param model: the model to be tested
    """
    x_train, x_test, y_train, y_test = data_preprocessing()
    predictions = model.predict(x_test)
    print("Accuracy: " + str(accuracy_score(y_test, predictions)))


def export_model(model):
    """
    Export the model
    :param model: the model to be exported
    :return: void function
    """
    joblib.dump(model, MODEL_PATH)

# x_train, x_test, y_train, y_test = data_preprocessing()
# testModel = rf_model()
# testModel.fit(x_train, y_train)
# test_accuracy(testModel)
# export_model(testModel)
