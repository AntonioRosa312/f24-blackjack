import pygame

CARD_WIDTH, CARD_HEIGHT = 100, 150

def cardFlip(screen, cardFront, cardBack, i, dealer): #i is the number of card in hand

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
            rotated_card = pygame.transform.rotate(cardFront, 180 - cardAngle)
            
        #screen.fill((0, 128, 0))
        screen.blit(pygame.image.load("screenshot.png"), (0,0))
        
        screen.blit(rotated_card, (x, y))
        pygame.display.flip()
        pygame.time.delay(20)

        if cardAngle == 180:
                break