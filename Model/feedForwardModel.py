import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from Database.modelDataGeneration import get_model_data


def data_preprocessing():
    """
    Data preprocessing for the model
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

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # sets device to gpu if available
input_size = 10  # number of features
hidden_size = 100  # Number of neurons in the hidden layer
num_classes = 2  # Number of classes in the dataset
num_epochs = 100  # Number of epochs for training
batch_size = 200  # Number of training samples used per step
learning_rate = 0.001  # Learning rate used in the optimizer

X_train, X_test, y_train, y_test = data_preprocessing()

train_loader = torch.utils.data.DataLoader(dataset=torch.utils.data.TensorDataset(torch.from_numpy(X_train).float(),
                                                                                  torch.from_numpy(y_train).long()),
                                           batch_size=batch_size, shuffle=True)  # create the training set

test_loader = torch.utils.data.DataLoader(dataset=torch.utils.data.TensorDataset(torch.from_numpy(X_test).float(),
                                                                                 torch.from_numpy(y_test).long()),
                                          batch_size=batch_size, shuffle=False)  # create the testing set


class NeuralNet(nn.Module):  # define the neural network
    def __init__(self, input_size, hidden_size, num_classes):  # define the layers
        super(NeuralNet, self).__init__()  # inherit the parent class
        self.l1 = nn.Linear(input_size, hidden_size)  # create the first layer
        self.relu = nn.ReLU()  # create the activation function
        self.l2 = nn.Linear(hidden_size, hidden_size)  # create the second layer
        self.l3 = nn.Linear(hidden_size, hidden_size)  # create the third layer
        self.l4 = nn.Linear(hidden_size, hidden_size)  # create the fourth layer
        self.l5 = nn.Linear(hidden_size, num_classes)  # create the fifth layer

    def forward(self, x):
        out = self.l1(x)  # pass the input through the first layer
        out = self.relu(out)  # pass the output through the activation function
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        out = self.relu(out)
        out = self.l4(out)
        out = self.relu(out)
        out = self.l5(out)
        return out  # return the output


model = NeuralNet(input_size, hidden_size, num_classes)  # create the neural network
criterion = nn.CrossEntropyLoss()  # create the loss function
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  # create the optimizer

n_total_steps = len(train_loader)  # total number of batches
for epoch in range(num_epochs):  # loop over the dataset multiple times
    for i, (data, labels) in enumerate(train_loader):
        data = data.reshape(-1, input_size).to(device)
        labels = labels.to(device)
        # forward pass: compute predicted outputs by passing inputs to the model
        outputs = model(data)
        loss = criterion(outputs, labels)
        # backward pass: compute gradient of the loss with respect to model parameters
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 != 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')

# Test the model
with torch.no_grad():
    n_correct = 0
    n_samples = 0
    for data, labels in test_loader:
        data = data.reshape(-1, input_size).to(device)
        labels = labels.to(device)
        outputs = model(data)
        _, predicted = torch.max(outputs.data, 1)
        n_samples += labels.size(0)
        n_correct += (predicted == labels).sum().item()

    acc = 100.0 * n_correct / n_samples  # accuracy in range 0 - 1
    print(f'Accuracy of the network: {acc}')
