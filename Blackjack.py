import pygame
import sys
import random

from CardDef import *
from ChipDef import *
#from generalDef import *
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
fontbig = pygame.font.Font(None, 56)

running_count = 0
#true_count = running_count/totalnumberofdecks

AI = argParse()
print(AI)



# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = CARD_VALUES[rank]
        self.placed = False
        self.image = assignCardImage(self)
        self.RCvalue = runningCountValue(self)

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']
                      for rank in CARD_VALUES.keys()]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


# game class
class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.money = 100
        self.game_over = False
        self.player_wins = 0
        self.currentbet = 0

    def bet(self, amount=0):
        if self.money <= 0:
            self.game_over = True
            exit
        
        print("Press the \'ENTER\' key to confirm bet")

        while True:
            ''' DISPLAY SECTION: BEGIN '''
            # display table
            screen.blit(pygame.transform.scale(pygame.image.load("table2.jpg"), (WIDTH, HEIGHT)), (0,0))
    
            # display chips on table
            for chip in chip_list:
                screen.blit(chip.image, chip.button)

            # display money
            money_surface = font.render(f"Balance: {self.money - amount}", True, WHITE)
            screen.blit(money_surface, (50, HEIGHT * .8))

            # display current bet
            curbet_surface = font.render(f"| Current Bet: {amount} ", True, WHITE)
            screen.blit(curbet_surface, (money_surface.get_width() + 60, HEIGHT * .8))

            # display "Press Enter"
            pressEnter_surface = fontbig.render("Press 'Enter' to Confirm Bet!", True, WHITE)
            screen.blit(pressEnter_surface, ((WIDTH - pressEnter_surface.get_width()) * .5, (HEIGHT - pressEnter_surface.get_height()) * .4))

            pygame.display.flip()
            ''' DISPLAY SECTION: END   '''

            mousepos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #check for keys
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and amount > 0: 
                        self.currentbet = amount
                        self.money -= amount
                        return
                    elif event.key == pygame.K_RETURN and amount <= 0:
                        print("You cannot bet $0, Try again.")

                #check for clicks    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #check all chips to see which ones were clicked
                    for chip in chip_list:
                        if chip.button_rect.collidepoint(mousepos):
                            print("BUTTON CLICKED")

                            # check if right click - this is to increase bet
                            if event.button == 1:
                                if (amount + chip.value <= self.money):
                                    amount += chip.value
                                    print(f"You just added ${chip.value}. Bet Total: ${amount}")
                                else:
                                    print("You do not have enough money to place that bet!, Try again.")   

                            # check if left click - this is to decrease bet        
                            elif event.button == 3:
                                if (amount - chip.value > 0):
                                    amount -= chip.value
                                    print(f"You just removed ${chip.value}. Bet Total: ${amount}")
                                else:
                                    amount = 0
                                    print("Your bet amount is now $0, Try adding some money to bet with.")
                
        
            # try:
            #     #amount = int(input(f"(Total Money = {self.money}) Enter Bet: \n"))
            #     amount = 10
            #     if amount > 0 and amount <= self.money:
            #         print(f"You just bet ${amount}\n")
            #         break
            #     else:
            #         print("The number must be greater than 0 and less than or equal to your money. Try again.")
            # except ValueError:
            #     print("That's not a valid number. Try again.")

        self.currentbet = amount
        self.money -= amount

    def deal_initlial(self):
        # Deal initial cards
        for _ in range(2):
            self.player_hand.append(self.deck.draw_card())
            self.dealer_hand.append(self.deck.draw_card())
            globals()["running_count"] += (self.player_hand[-1].RCvalue + self.dealer_hand[-1].RCvalue)

    def calculate_score(self, hand):
        score = sum(card.value for card in hand)
        # Adjust for Aces
        aces = sum(1 for card in hand if card.rank == "ace")
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def player_hit(self):
        if not self.game_over:
            self.player_hand.append(self.deck.draw_card())
            globals()["running_count"] += self.player_hand[-1].RCvalue 

            if self.calculate_score(self.player_hand) > 21:
                self.game_over = True

    def dealer_play(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw_card())
            globals()["running_count"] += self.dealer_hand[-1].RCvalue

        self.game_over = True

    def check_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        if player_score > 21:
            # do nothing, current bet already subtracted from total money
            return "Player Busts! Dealer Wins!"
        elif dealer_score > 21 or player_score > dealer_score:
            self.player_wins += 1
            self.money += (2 * self.currentbet) # add 2xcurrentbet to total money
            return "Player Wins!"
        elif player_score < dealer_score:
            # do nothing, current bet already subtracted from total money
            return "Dealer Wins!"
        else:
            self.money += self.currentbet # add back currentbet to total money
            return "It's a Tie!"


# Initialize the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("368 Blackjack")
clock = pygame.time.Clock()

game = Blackjack()
screen.blit(pygame.transform.scale(pygame.image.load("table2.jpg"), (WIDTH, HEIGHT)), (0,0))    

# display chips on table
for chip in chip_list:
    screen.blit(chip.image, chip.button)

game.deal_initlial()
pygame.display.flip()

game.bet()


# Main game loop
running = True
while running:
    
    # display table
    screen.blit(pygame.transform.scale(pygame.image.load("table2.jpg"), (WIDTH, HEIGHT)), (0,0))
    
    # display chips on table
    for chip in chip_list:
        screen.blit(chip.image, chip.button)

    mousepos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:  # Hit
                game.player_hit()
            if event.key == pygame.K_s:  # Stand
                game.dealer_play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for chip in chip_list:
                if chip.button_rect.collidepoint(mousepos):
                    print("BUTTON CLICKED")


   
    # Draw the hands
    '''
    To fix dealer card flip removing players hand during animation, combine both dealer hand and player hand list, 
    sort from already placed to not placed, first screen blit all the placed cards(dealer hand first, then player hand), then placed all unplaced cards (card flip) 
    '''
    for i, card in enumerate(game.dealer_hand):
        if(not card.placed):
            pygame.image.save(screen, "screenshot.png")
            cardFlip(screen, card, i, True)
            card.placed = True
        else: 
            screen.blit(card.image, ((50 + i * (CARD_WIDTH + 10), 100) ))


    for i, card in enumerate(game.player_hand):
        if(not card.placed):
            pygame.image.save(screen, "screenshot.png")
            #cardSlide(screen, (WIDTH,HEIGHT), i, False)
            cardFlip(screen, card, i, False)
            card.placed = True
        else: 
            screen.blit(card.image, ( (600 + i * (CARD_WIDTH - 50)), (550 - i * (CARD_HEIGHT- 100)) ) )

    # display chips on table
    for chip in chip_list:
        screen.blit(chip.image, chip.button)

    # for i, card in enumerate(game.dealer_hand):
    #     pygame.draw.rect(screen, WHITE, (50 + i * (CARD_WIDTH + 10), 100, CARD_WIDTH, CARD_HEIGHT))
    #     # You can add text here to display card rank/suit

    # get scores
    player_score = game.calculate_score(game.player_hand)
    dealer_score = game.calculate_score(game.dealer_hand)
   
    # display score
    text_surface = font.render(f"Player Score: {player_score} | Dealer Score: {dealer_score}", True, WHITE)
    screen.blit(text_surface, (50, 50))

    # display running count
    RC_surface = font.render(f"This is RUNNING COUNT: {running_count}", True, WHITE)
    screen.blit(RC_surface, (400,100))

    # display money
    money_surface = font.render(f"Balance: {game.money}", True, WHITE)
    screen.blit(money_surface, (50, HEIGHT * .8))

    # display current bet
    curbet_surface = font.render(f"| Current Bet: {game.currentbet} ", True, WHITE)
    screen.blit(curbet_surface, (money_surface.get_width() + 60, HEIGHT * .8))


    # Check for game over
    if game.game_over:
        result_text = game.check_winner()
        result_surface = font.render(result_text, True, WHITE)
        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT // 2))
        print(f"MONI {game.money}\n")
        #screen.blit(money_surface, (50, HEIGHT * .85))

        pygame.display.flip()
        pygame.time.wait(2000)
        # Reset player and dealer hands, deal 2 new cards to each 
        game.player_hand = []
        game.dealer_hand = []
        # re-display money after game over
        #money_surface = font.render(f"Balance: {game.money}", True, WHITE)
        #screen.blit(money_surface, (50, HEIGHT * .8))
        # get a new bet
        game.bet()
        # deal a new starting hand
        game.deal_initlial()
        # restart game
        game.game_over = not game.game_over

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
