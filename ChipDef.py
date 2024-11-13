import pygame
import os
import sys


class Chip:
    def __init__(self, chip_value):
        self.value = chip_value
        self.image = ""

        self.white_chip = 1
        self.red_chip = 5
        self.green_chip = 25


def startScreen(screen):

    WIDTH, HEIGHT = screen.get_size()

    font = pygame.font.Font(None, 56)
    WHITE = (255, 255, 255)

    screen.blit(pygame.transform.scale(pygame.image.load("casino-photo.jpg"), (WIDTH, HEIGHT)), (0,0))
    pygame.display.set_caption("Blackjack Start Screen")

    title = font.render("Enter Money to Play", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    pygame.display.flip()
    pygame.time.wait(4000)
    #while True:
            
    #     for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()

    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 # If the mouse is clicked on the button, proceed
    #                 if button_rect.collidepoint(event.pos):
    #                     if input_text.isdigit() and int(input_text) > 0:
    #                         print(f"Starting game with ${input_text}!")
    #                         return int(input_text)  # Return the entered amount as an integer
    #                     else:
    #                         print("Invalid input! Enter a valid amount.")
    #                         input_text = ""  # Reset input if it's invalid

    #             if event.type == pygame.KEYDOWN:
    #                 if event.unicode.isdigit():  # Accept only digits
    #                     input_text += event.unicode  # Add the typed character to the input text
    #                 elif event.key == pygame.K_BACKSPACE:
    #                     input_text = input_text[:-1]  # Remove last character if backspace is pressed
    #                 elif event.key == pygame.K_RETURN:
    #                     if input_text.isdigit() and int(input_text) > 0:
    #                         print(f"Starting game with ${input_text}!")
    #                         return int(input_text)  # Start the game with the entered amount
    #                     else:
    #                         print("Invalid input! Enter a valid amount.")
    #                         input_text = ""  # Reset input if it's invalid