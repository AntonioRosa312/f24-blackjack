import pygame
import sys
import random

from CardDef import *
#PLAYING CARDS https://code.google.com/archive/p/vector-playing-cards/downloads

# Initialize Pygame
pygame.init()

# Get screen information
info = pygame.display.Info()

# Access screen width and height
WIDTH = info.current_w - 300
HEIGHT = info.current_h - 100


# Constants
FPS = 30
CARD_WIDTH, CARD_HEIGHT = 100, 150

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

CARD_IMAGES = {
    
}

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = CARD_VALUES[rank]
        self.placed = False

    def assignCard(self):
        


    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for rank in CARD_VALUES.keys()]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Game class
class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False

        # Deal initial cards
        for _ in range(2):
            self.player_hand.append(self.deck.draw_card())
            self.dealer_hand.append(self.deck.draw_card())

    def calculate_score(self, hand):
        score = sum(card.value for card in hand)
        # Adjust for Aces
        aces = sum(1 for card in hand if card.rank == 'A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def player_hit(self):
        if not self.game_over:
            self.player_hand.append(self.deck.draw_card())
            if self.calculate_score(self.player_hand) > 21:
                self.game_over = True

    def dealer_play(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw_card())
        self.game_over = True

    def check_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        if player_score > 21:
            return "Player Busts! Dealer Wins!"
        elif dealer_score > 21 or player_score > dealer_score:
            return "Player Wins!"
        elif player_score < dealer_score:
            return "Dealer Wins!"
        else:
            return "It's a Tie!"

# Initialize the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("368 Blackjack")
clock = pygame.time.Clock()
game = Blackjack()

# Main game loop
running = True
while running:
    
    screen.blit(pygame.transform.scale(pygame.image.load("table2.jpg"), (WIDTH, HEIGHT)), (0,0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:  # Hit
                game.player_hit()
            if event.key == pygame.K_s:  # Stand
                game.dealer_play()

    image = pygame.transform.scale(pygame.image.load("PNG-cards-1.3/2_of_clubs.png"), (CARD_WIDTH, CARD_HEIGHT))
    image2 = pygame.transform.scale(pygame.image.load("PNG-cards-1.3/card_image.png"), (CARD_WIDTH, CARD_HEIGHT))
    # Draw the hands
    for i, card in enumerate(game.dealer_hand):
        if(not card.placed):
            #pygame.image.save(screen, 'screenshot.png')
            pygame.image.save(screen, "screenshot.png")
            cardFlip(screen, image, image2, i, True)
            card.placed = True
        else: 
            screen.blit(image, ((50 + i * (CARD_WIDTH + 10), 100) ))
        #pygame.draw.rect(screen, WHITE, (50 + i * (CARD_WIDTH + 10), 100, CARD_WIDTH, CARD_HEIGHT))



    for i, card in enumerate(game.player_hand):
        if(not card.placed):
            #pygame.image.save(screen, 'screenshot.png')
            pygame.image.save(screen, "screenshot.png")
            cardFlip(screen, image, image2, i, False)
            card.placed = True
        else: 
            screen.blit(image, ( (600 + i * (CARD_WIDTH - 50)), (550 - i * (CARD_HEIGHT- 100)) ) )
        #pygame.draw.rect(screen, WHITE, (600 + i * (CARD_WIDTH - 50), (550 - i * (CARD_HEIGHT- 100)), CARD_WIDTH, CARD_HEIGHT))


    # for i, card in enumerate(game.dealer_hand):
    #     pygame.draw.rect(screen, WHITE, (50 + i * (CARD_WIDTH + 10), 100, CARD_WIDTH, CARD_HEIGHT))
    #     # You can add text here to display card rank/suit

    # Display scores
    player_score = game.calculate_score(game.player_hand)
    dealer_score = game.calculate_score(game.dealer_hand)
    score_text = f"Player Score: {player_score} | Dealer Score: {dealer_score}"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(score_text, True, WHITE)
    screen.blit(text_surface, (50, 50))

    # Check for game over
    if game.game_over:
        result_text = game.check_winner()
        result_surface = font.render(result_text, True, WHITE)
        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
