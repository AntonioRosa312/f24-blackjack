import torch
import torch.nn as nn
#import torchvision
#from torch.utils.data import DataLoader
#from tqdm import tqdm
#import matplotlib.pyplot as plt
import torch.nn.functional as F



# (playerscore, dealerscore, truecount)
# Illustrious18 = {(16,10,0): "stand", }


# def AIdecision():
#     if(playerhand <= 11):
#         return "hit"
#     print("Hi")



# create the model class using the nn.Module
class MyNet(nn.Module):
    # Input layer (player total, dealer total, running count) -->
    # Hidden layer 1 (number of nuerons) -->
    # Hideen layer 2 (number of nuerons) -->
    # Output (action [stand, hit])

                                # set size of hidden layers 1 & 2
    def __init_(self, input_features = 3, HL1 = 32, HL2 = 32, output_features = 2):
        super(MyNet, self).__init__()
   
        self.fc1 = nn.Linear(input_features, HL1)
        self.fc2 = nn.Linear(HL1, HL2)
        self.out = nn.Linear(HL2, output_features)
    
    def forward(self, x):
        x = nn.ReLU(self.fc1(x))
        x = nn.ReLU(self.fc2(x))
        x = self.out(x)
        return x


torch.manual_seed(1000)
network = MyNet()

# train test split X,Y
X = my_df.drop("action", axis = 1)
Y = my_df["action"]
# convert to numpy arrays
X = X.values
Y = Y.values

from sklearn.model_selection import train_test_split
# train test split                                        test_size = 20%, train_size = 80%
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = .2)

# convert X features to float tensors
X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)

# convert Y features to float tensors
Y_train = torch.FloatTensor(Y_train)
Y_test = torch.FlaotTensor(Y_test)

# set criterion of network to measure the error, how far off the predictions are from the data
criterion = nn.CrossEntropyLoss()
# optimizer (Adam) and learning rate (if error doesn't go down after a bunch of iterations (epochs), lower our learning rate)
optimizer = torch.optim.Adam(network.parameters(), lr = .01)

losses = []
# train the network, each epoch is a run through our network with all the data
for epoch in range(10):
    # go forward and get a prediction
    Y_prediction = network.forward(X_train) # get predicted results

    # measure the loss/error, going to be high at first
    loss = criterion(Y_prediction, Y_train) # predicted values vs Y_train values

    # keep track of losses
    losses.append(loss)

    # print every epoch
    print(f"Epoch #{epoch} and loss: {loss}")

    # do some back propagation which takes the error rate of forward propagation and feeds it back through the network to fine tune the weights
    # zero out the gradients
    optimizer.zero_grad()
    # do the backward pass
    loss.backward()
    # take a step with the optimizer
    optimizer.step()