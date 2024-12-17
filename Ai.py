import torch
import torch.nn as nn
#import torchvision
#from torch.utils.data import DataLoader
#from tqdm import tqdm
#import matplotlib.pyplot as plt
import torch.nn.functional as F
import numpy as np
from sklearn.model_selection import train_test_split
import random
import csv
import pandas as pd

from CardDef import CARD_VALUES



# simulate a 1 deck blackjack game and record data
class BlackjackSimulation:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.running_count = 0
        self.deck = self.createDeck()
        self.game_over = False
        self.player_wins = 0

    def createDeck(self):
        thisdeck = []
        for cardvalue in CARD_VALUES.values():
            for _ in range(4): # there are 4 cards with the same value/face per deck
                thisdeck.append(cardvalue)
        random.shuffle(thisdeck)
        return thisdeck
    
    
    def updateRC(self, cardvalue):
        # adjust running count for card being sent through
        if cardvalue >= 2 and cardvalue <= 6: self.running_count += 1
        elif cardvalue == 1 or cardvalue >= 10: self.running_count -= 1


    def reset(self, code=""):
        if code == "full":
            self.deck = self.createDeck()
            self.running_count = 0

        self.player_hand = []
        self.dealer_hand = []


    def deal_initlial(self):
        # deal random initial cards, from values 1-10, to make more complex, could incorporate card suits and an actual deck of cards,
        # but since we are having our AI determine based on player hand total and dealer hand total this will do just fine
        for i in range(2):
            if len(self.deck) < 2: return "empty"
            self.player_hand.append(self.deck.pop())
            self.dealer_hand.append(self.deck.pop())
            self.updateRC(self.player_hand[i])
            self.updateRC(self.dealer_hand[i])
        
        if self.player_hand == 21 or self.dealer_hand == 21: 
            return "21"


    def check_winner(self, action):

        if action==1:
            card = self.deck.pop()
            if (sum(self.player_hand) + card) > 21: 
                winloss = 0 #if the player bust then its considered a loss/bad move
                #data.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count, winloss, action] )
            else: 
                winloss = 1 #if player can hit and not bust, then its a good move
                
                #data.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count, winloss, action] )
                #self.player_hand.append(card) #since you can add this card to players hand with out a bust, then do that and keep going on with that hand for more data


        #check for stand
        if action==0:
            card = None
            if sum(self.dealer_hand) > sum(self.player_hand):
                winloss = 0
            # card = self.deck.pop()
            # if (sum(self.dealer_hand) + card) > sum(self.player_hand) and (sum(self.dealer_hand) + card) < 21: 
            #     winloss = 0 #if the dealer bust then its considered a loss/bad move
            #     return winloss
            #     data.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count, winloss, action] )
            else: 
                winloss = 1 #if player can hit and not bust, then its a good move
                #data.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count, winloss, action] )
                #self.player_hand.append(card) #since you can add this card to players hand with out a bust, then do that and keep going on with that hand for more data
        
        return winloss, card


    # for the initial 4 cards, there are 52P4 (52 permute 4) = 6,497,400 possibilities,
    # we will just run through 1000(samples) possibilities.
    def getData(self, samples = 1000):
        data = []
        for _ in range(samples):
            
            match self.deal_initlial():
                # if we run into the issue of running out of cards for the 1 deck, then simply restart 
                case "empty":
                    self.reset("full")
                    self.deal_initlial()
                # if we run into the issue of dealing a 21 for either player or dealer, then simply deal a new hand
                case "21":
                    self.reset()
                    self.deal_initlial()
                case _: pass
            

            while (sum(self.player_hand) < 21):
                # having stand and hit as integers is better for nn processing
                action = random.choice([0, 1]) #stand = 0, hit = 1

                if (not self.deck): break #if deck is empty, break out of while loop where it will do a reset(full)

                winloss, cardpopped = self.check_winner(action)

                data.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count, winloss, action] )
                
                # if action=1=hit and the deck is not empty, then append card to players hand
                if action: 
                    self.player_hand.append(cardpopped)
                    self.updateRC(self.player_hand[-1]) #same thing as cardpopped
                else: break

            self.reset()

        return data

    # runs the simulation and stores data into a local csv file
    def storeData(self):
        fieldnames = ["Player score", "Dealer score", "Running count", "WinLoss", "Action"]
        data = self.getData(1000)
        
        with open("BlackjackSimulationData.csv", 'w') as file:
            csv.writer(file).writerow(fieldnames)
            csv.writer(file).writerows(data)
        
    def retrieveData(self):
        data = pd.read_csv("BlackjackSimulationData.csv")
        print(data.head())
        print(f"\nlength of data: {len(data)}\n")
        return data





# create the model class using the nn.Module
class MyNet(nn.Module):
    # Input layer (player total, dealer total, running count, winloss) -->
    # Hidden layer 1 (number of nuerons) -->
    # Hideen layer 2 (number of nuerons) -->
    # Output (action [stand, hit])

                                # set size of hidden layers 1 & 2
    def __init__(self, input_features = 4, HL1 = 32, HL2 = 32, output_features = 2):
        super(MyNet, self).__init__()
   
        # self.fc1 = nn.Linear(input_features, HL1)
        # self.fc2 = nn.Linear(HL1, HL2)
        # self.out = nn.Linear(HL2, output_features)
        
        self.nn = nn.Sequential(
            nn.LazyLinear(input_features, HL1),
            nn.ReLU(),
            nn.LazyLinear(HL1, HL2),
            nn.ReLU(),
            nn.LazyLinear(HL2, output_features)
        )
    def forward(self, x):
        # x = nn.ReLU(self.fc1(x))
        # x = nn.ReLU(self.fc2(x))
        # x = self.out(x)
        # return x
        return self.nn(x)



def trainNetwork(data, network):
    torch.manual_seed(1000)
    # train & test split, X,y                                 
    X = data[["Player score", "Dealer score", "Running count", "WinLoss"]]
    y = data["Action"]

    # convert to numpy arrays
    X = X.values
    y = y.values

    # train test split                                        test_size = 30%, train_size = 70%
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = .7)#test_size = .3)


    # # convert X features to tensors
    # X_train = torch.tensor(X_train)
    # X_test = torch.tensor(X_test)

    # # convert y features to tensors
    # y_train = torch.tensor(y_train)
    # y_test = torch.tensor(y_test)


    # convert X features to float tensors
    X_train = torch.FloatTensor(X_train)
    X_test = torch.FloatTensor(X_test)

    # convert Y features to long tensors
    y_train = torch.LongTensor(y_train)
    y_test = torch.LongTensor(y_test)

    # set criterion of network to measure the error, how far off the predictions are from the data
    criterion = nn.CrossEntropyLoss()
    #criterion = nn.MSELoss

    # optimizer (Adam) and learning rate (if error doesn't go down after a bunch of iterations (epochs), lower our learning rate)
    optimizer = torch.optim.Adam(network.parameters(), lr=.01)

    losses = []
    # train the network, each epoch is a run through our network with all the data
    for epoch in range(50):
        # go forward and get a predictionA
        y_prediction = network.forward(X_train) # get predicted results

        # measure the loss/error, going to be high at first
        loss = criterion(y_prediction, y_train) # predicted values vs Y_train values

        # keep track of losses
        #loss is a tensor, transform back to numpy array
        losses.append(loss.detach().numpy())

        # print every epoch to see stabilization 
        print(f"Epoch #{epoch} and loss: {loss}")

        # do some back propagation which takes the error rate of forward propagation and feeds it back through the network to fine tune the weights
        # zero out the gradients
        optimizer.zero_grad()
        # do the backward pass
        loss.backward()
        # take a step with the optimizer
        optimizer.step()


# send test data into model, without adjusting any weights
# with torch.no_grad(): # this turns off back propogration so it doesn't go backwards into model and mess with the weights
#     y_evaluation = network.forward(X_test) #send test data through network
#     losss= criterion(y_evaluation, y_test)
#     print(losss)

def sendToNetwork(gamestate, network):
    #gamestate consists of ["Player score", "Dealer score", "Running count", "WinLoss"], ex. [20, 17, 3, 1]
    with torch.no_grad(): # this turns off back propogration so it doesn't go backwards into model and mess with the weights
        #test_input = torch.FloatTensor([gamestate])  # Ensure 2D input
        test_output = network(torch.FloatTensor([gamestate]))
        action = torch.argmax(test_output, dim=1).item()
        print(f"With gamestate: {gamestate} Custom Input Prediction: {action} (0=Stand, 1=Hit)")
        return action
