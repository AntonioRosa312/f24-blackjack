import torch
import torch.nn as nn
#import torchvision
#from torch.utils.data import DataLoader
#from tqdm import tqdm
#import matplotlib.pyplot as plt
import torch.nn.functional as F
import numpy as np
import random
import json



# (playerscore, dealerscore, truecount)
# Illustrious18 = {(16,10,0): "stand", }


# def AIdecision():
#     if(playerhand <= 11):
#         return "hit"
#     print("Hi")


class BlackjackSimulation:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.running_count = 0
        self.game_over = False
        self.player_wins = 0

    def reset(self):
        self.player_hand = []
        self.dealer_hand = []
        self.running_count = 0


    def deal_initlial(self):
        # deal random initial cards, from values 1-10, to make more complex, could incorporate card suits and an actual deck of cards,
        # but since we are having our AI determine based on player hand total and dealer hand total this will do just fine
        for i in range(2):
            self.player_hand.append(random.randint(1,10))
            self.dealer_hand.append(random.randint(1,10))
            # adjust running count for player card[i]
            if self.player_hand[i] >= 2 and self.player_hand[i] <= 6: self.running_count += 1
            elif self.player_hand[i] == 1 or self.player_hand == 10: self.running_count -= 1
            # adjust running count for dealer card[i]
            if self.dealer_hand[i] >= 2 and self.dealer_hand[i] <= 6: self.running_count += 1
            elif self.dealer_hand[i] == 1 or self.dealer_hand == 10: self.running_count -= 1

        
        if self.player_hand == 21 or self.dealer_hand == 21: 
            self.game_over = True


    # for the initial 4 cards, there are 52P4 (52 permute 4) = 6,497,400 possibilities,
    # we will just run through 10000(samples) possibilities.
    def getData(self, samples = 100):
        X, Y = [], []
        for _ in range(samples):
            print("working")
            self.deal_initlial()
            while (sum(self.player_hand) < 21):
                # having stand and hit as integers is better for nn processing
                action = random.choice([0, 1]) #stand = 0, hit = 1

                ''' send action into a calculate win/loss function and pass to Y ?'''

                # append [player_score, dealer_score, running_count]
                X.append( [sum(self.player_hand), sum(self.dealer_hand), self.running_count] )
                # append action
                Y.append(action)

                if action: self.player_hand.append(random.randint(1,10))
                else: break

            self.reset()
        
        return (X,Y)

    # runs the simulation and stores data into a local json file
    def storeData(self):
        X, Y = self.getData(100)
        data = {"X values": X, "Y values": Y}
        with open("BlackjackSimulationData.json", "w") as file:
            json.dump(data, file)







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
'''
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

    '''