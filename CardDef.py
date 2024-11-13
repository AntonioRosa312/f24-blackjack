import pygame
import os
import sys

# Card Dimensions
CARD_WIDTH, CARD_HEIGHT = 100, 150
cardBack = pygame.transform.scale(pygame.image.load("PNG-cards-1.3/card_image.png"), (CARD_WIDTH, CARD_HEIGHT))

# Load card files from called directory
cardfiles = [f for f in os.listdir("PNG-cards-1.3")] 
cardfiles = [f for f in cardfiles if len(f.split('_')) == 3 ] #or notUsed.append(f)]

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'jack': 10, 'queen': 10, 'king': 10, 'ace': 11
}



def cardFlip(screen, card, i, dealer): #i is the number of card in hand

    if(dealer):
         x,y = (50 + i * (CARD_WIDTH + 10), 100)
    else:
         x,y = ( (600 + i * (CARD_WIDTH - 50)), (550 - i * (CARD_HEIGHT- 100)) )

    cardAngle = 0
    flipSpeed = 5

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
        # Update the angle for flipping
        cardAngle += flipSpeed  # Increase the angle for flip
    
        #update card based on angle
        if cardAngle < 90:
            # Show the front card, rotated
            rotated_card = pygame.transform.rotate(cardBack, cardAngle)
        else:
            # Show the back card, rotated
            rotated_card = pygame.transform.rotate(card.image, 180 - cardAngle)
            
        screen.blit(pygame.image.load("screenshot.png"), (0,0))
        
        screen.blit(rotated_card, (x, y))
        pygame.display.flip()
        pygame.time.delay(20)

        if cardAngle == 180:
            break


def cardSlide(screen, screensize, i, dealer):

    cardPos = [screensize[0] / 2, 0]
    speed = 1
    ticks = 30
    # Checks if card is a dealer or player card, sets Final card location to designated position
    if(dealer):
         FinalPos = (50 + i * (CARD_WIDTH + 10), 100)
    else:
         FinalPos = ( (600 + i * (CARD_WIDTH - 50)), (550 - i * (CARD_HEIGHT- 100)) )

    changeinX = FinalPos[0]/ticks
    changeinY = FinalPos[1]/ticks
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

        if cardPos == FinalPos:
            break
        else:
            cardPos[0] += changeinX
            cardPos[1] += changeinY
        #change in x
        # if(cardPos[0] > FinalPos[0]): cardPos[0] -= speed
        # elif(cardPos[0] < FinalPos[0]): cardPos[0] += speed
        # #change in y
        # if(cardPos[1] > FinalPos[1]): cardPos[1] -= speed
        # elif(cardPos[1] < FinalPos[1]): cardPos[1] += speed

        screen.blit(pygame.image.load("screenshot.png"), (0,0))
        screen.blit(cardBack, cardPos)
        pygame.display.flip()
        pygame.time.delay(2)


        #to make a smoother transition do FinalPos[x] - cardPos[x] / speed 
        #to make a smoother transition do FinalPos[y] - cardPos[y] / speed 
        # change of rate of x added to card and change of rate of y added to card for each tick speed


def assignCardImage(card):
    cardimage = [thiscard for thiscard in cardfiles if (card.rank in thiscard and card.suit.lower() in thiscard)]
    cardimage.sort()
    return pygame.transform.scale(pygame.image.load("PNG-cards-1.3/" + cardimage[0]), (CARD_WIDTH, CARD_HEIGHT))

def runningCountValue(card):
    if CARD_VALUES[card.rank] >= 2 and CARD_VALUES[card.rank] <= 6: return 1
    elif CARD_VALUES[card.rank] >= 7 and CARD_VALUES[card.rank] <= 9: return 0
    else: return -1