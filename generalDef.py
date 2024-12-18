import pygame
import sys
import random

from ChipDef import *
#PLAYING CARDS https://code.google.com/archive/p/vector-playing-cards/downloads
#https://wizardofodds.com/games/blackjack/card-counting/high-low/
#https://www.vecteezy.com/vector-art/1609940-poker-chips-set-isolated-white-background

# Initialize Pygame
pygame.init()

# Get screen information
info = pygame.display.Info()

# Access screen width and height
WIDTH = info.current_w - 300
HEIGHT = info.current_h - 100

FPS = 30

WHITE = (255, 255, 255)

font = pygame.font.Font(None, 36)

running_count = 0
#true_count = running_count/totalnumberofdecks

#AI = argParse()
#print(AI)

pygame.quit()