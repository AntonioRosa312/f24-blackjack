import pygame
import os

# Card Dimensions
CARD_WIDTH, CARD_HEIGHT = 100, 150
cardBack = pygame.transform.scale(pygame.image.load("PNG-cards-1.3/card_image.png"), (CARD_WIDTH, CARD_HEIGHT))

# Load card files from called directory
cardfiles = [f for f in os.listdir("PNG-cards-1.3")] 
cardfiles = [f for f in cardfiles if len(f.split('_')) == 3 ] #or notUsed.append(f)]



def cardFlip(screen, card, i, dealer): #i is the number of card in hand

    if(dealer):
         x,y = (50 + i * (CARD_WIDTH + 10), 100)
    else:
         x,y = ( (600 + i * (CARD_WIDTH - 50)), (550 - i * (CARD_HEIGHT- 100)) )

    cardAngle = 0
    flipSpeed = 5

    while(True):
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

    if(dealer):
         FinalPos = (50 + i * (CARD_WIDTH + 10), 100)
    else:
         FinalPos = ( (600 + i * (CARD_WIDTH - 50)), (550 - i * (CARD_HEIGHT- 100)) )

    changeinX = FinalPos[0]/ticks
    changeinY = FinalPos[1]/ticks
    while(True):
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