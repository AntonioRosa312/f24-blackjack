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


# (playerscore, dealerscore, truecount)
# Illustrious18 = {(16,10,0): "stand", }


# def AIdecision():
#     if(playerhand <= 11):
#         return "hit"
#     print("Hi")

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
    
    # def popDeck(self):
    #     #if deck is empty, reshuffle a new deck
    #     if not self.deck: 
    #         self.deck = self.createDeck()
    #         return "empty"

    #     card = self.deck.pop()
    #     return card  
    
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
        '''
            # adjust running count for player card[i]
            if cardvalue >= 2 and cardvalue <= 6: self.running_count += 1
            elif cardvalue == 1 or cardvalue >= 10: self.running_count -= 1
            # adjust running count for dealer card[i]
            if cardvalue >= 2 and cardvalue <= 6: self.running_count += 1
            elif cardvalue == 1 or cardvalue >= 10: self.running_count -= 1
        '''
        
        if self.player_hand == 21 or self.dealer_hand == 21: 
            self.game_over = True


    # for the initial 4 cards, there are 52P4 (52 permute 4) = 6,497,400 possibilities,
    # we will just run through 1000(samples) possibilities.
    def getData(self, samples = 1000):
        data = []
        for _ in range(samples):
            #print(f"working - deck length: {len(self.deck)}")
            
            # if we run into the issue of running out of cards for the 1 shoe, then simply restart 
            if self.deal_initlial() == "empty":
                self.reset("full")
                self.deal_initlial()

            while (sum(self.player_hand) < 21):
                # having stand and hit as integers is better for nn processing
                action = random.choice([0, 1]) #stand = 0, hit = 1

                ''' send action into a calculate win/loss function and pass to Y ?'''

                # append [player_score, dealer_score, running_count, action]
                data.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count, action] )

                # if action=1=hit and the deck is not empty, then append card to players hand
                if action and self.deck: 
                    self.player_hand.append(self.deck.pop())
                    self.updateRC(self.player_hand[-1])
                else: break

            self.reset()

        return data

    # runs the simulation and stores data into a local csv file
    def storeData(self):
        fieldnames = ["Player score", "Dealer score", "Running count", "Action"]
        data = self.getData(1000)
        
        with open("BlackjackSimulationData.csv", 'w') as file:
            csv.writer(file).writerow(fieldnames)
            csv.writer(file).writerows(data)
        
    def retrieveData(self):
        data = pd.read_csv("BlackjackSimulationData.csv")
        print(data.head())
        print(f"\nlength of data: {len(data)}\n")
        return data



# playerhand, dealerhand, running counting, (action, win/loss)



    # def calculate_score(self, hand):
    #     score = sum(card.value for card in hand)
    #     # Adjust for Aces
    #     aces = sum(1 for card in hand if card.rank == "ace")
    #     while score > 21 and aces:
    #         score -= 10
    #         aces -= 1
    #     return score

    # def player_hit(self):
    #     if not self.game_over:
    #         self.player_hand.append(self.deck.draw_card())
    #         globals()["running_count"] += self.player_hand[-1].RCvalue 

    #         if self.calculate_score(self.player_hand) >= 21:
    #             self.game_over = True

    # def dealer_play(self):
    #     while self.calculate_score(self.dealer_hand) < 17:
    #         self.dealer_hand.append(self.deck.draw_card())
    #         globals()["running_count"] += self.dealer_hand[-1].RCvalue

    #     self.game_over = True

    # def check_winner(self):
    #     player_score = self.calculate_score(self.player_hand)
    #     dealer_score = self.calculate_score(self.dealer_hand)
    #     if player_score > 21:
    #         # do nothing, current bet already subtracted from total money
    #         return "Player Busts! Dealer Wins!"
    #     elif dealer_score > 21 or player_score > dealer_score or player_score == 21:
    #         self.player_wins += 1
    #         self.money += (2 * self.currentbet) # add 2xcurrentbet to total money
    #         return "Player Wins!"
    #     elif player_score < dealer_score or dealer_score == 21:
    #         # do nothing, current bet already subtracted from total money
    #         return "Dealer Wins!"
    #     else:
    #         self.money += self.currentbet # add back currentbet to total money
    #         return "It's a Tie!"


# create the model class using the nn.Module
class MyNet(nn.Module):
    # Input layer (player total, dealer total, running count) -->
    # Hidden layer 1 (number of nuerons) -->
    # Hideen layer 2 (number of nuerons) -->
    # Output (action [stand, hit])

                                # set size of hidden layers 1 & 2
    def __init__(self, input_features = 3, HL1 = 32, HL2 = 32, output_features = 2):
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


torch.manual_seed(100)
network = MyNet()

print(f"This is network param: {list(network.parameters())}")


BlackjackDATA = BlackjackSimulation()
BlackjackDATA.storeData()
data = BlackjackDATA.retrieveData()

# train & test split, X,y                                 #"WinLoss"
X = data[["Player score", "Dealer score", "Running count"]]#my_df.drop("action", axis = 1)
print(X)
y = data["Action"]
print(y)
# convert to numpy arrays
X = X.values
y = y.values
print(y)

# train test split                                        test_size = 20%, train_size = 80%
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = .7)#test_size = .2)



# # convert X features to tensors
# X_train = torch.tensor(X_train)
# X_test = torch.tensor(X_test)

# # convert y features to tensors
# y_train = torch.tensor(y_train)
# y_test = torch.tensor(y_test)


# convert X features to float tensors
X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)

# convert Y features to float tensors
y_train = torch.FloatTensor(y_train)
y_test = torch.FloatTensor(y_test)

# set criterion of network to measure the error, how far off the predictions are from the data
criterion = nn.CrossEntropyLoss()
#criterion = nn.MSELoss

# optimizer (Adam) and learning rate (if error doesn't go down after a bunch of iterations (epochs), lower our learning rate)
optimizer = torch.optim.Adam(network.parameters(), lr=.01)

losses = []
# train the network, each epoch is a run through our network with all the data
for epoch in range(10):
    # go forward and get a prediction
    y_prediction = network.forward(X_train) # get predicted results

    # measure the loss/error, going to be high at first
    loss = criterion(y_prediction, y_train) # predicted values vs Y_train values

    # keep track of losses
    #loss is a tensor, transform back to numpy array
    losses.append(loss.detach().numpy())

    # print every epoch
    print(f"Epoch #{epoch} and loss: {loss}")

    # do some back propagation which takes the error rate of forward propagation and feeds it back through the network to fine tune the weights
    # zero out the gradients
    optimizer.zero_grad()
    # do the backward pass
    loss.backward()
    # take a step with the optimizer
    optimizer.step()

