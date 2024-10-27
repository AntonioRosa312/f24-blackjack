import pygame
import sys

# Initialize Pygame
pygame.init()
CARD_WIDTH, CARD_HEIGHT = 100, 150
# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Animated Card Flip Example')

# Load the card images (front and back)
card_front = pygame.transform.scale(pygame.image.load("PNG-cards-1.3/2_of_clubs.png"), (CARD_WIDTH, CARD_HEIGHT))
card_back = pygame.transform.scale(pygame.image.load("PNG-cards-1.3/playing-cards-back.jpg"), (CARD_WIDTH, CARD_HEIGHT))


# Card settings
card_rect = card_front.get_rect(center=(width // 2, height // 2))
flipped = False
angle = 0
flip_speed = 5  # Speed of the flip animation
flip_duration = 30  # Total frames for the flip

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if card_rect.collidepoint(event.pos):
                flipped = not flipped
                angle = 0  # Reset angle on flip

    # Clear the screen
    screen.fill((0, 128, 0))  # White background

    # Update the angle for flipping
    if flipped:
        if angle < 180:
            angle += flip_speed  # Increase the angle for flip
    else:
        if angle > 0:
            angle -= flip_speed  # Decrease the angle for flip

    # Draw the card based on the flip state
    if angle < 90:
        # Show the front card, rotated
        rotated_card = pygame.transform.rotate(card_front, angle)
    else:
        # Show the back card, rotated
        rotated_card = pygame.transform.rotate(card_back, 180 - angle)

    # Adjust the rect for the rotated image
    rotated_rect = rotated_card.get_rect(center=card_rect.center)

    # Draw the rotated card
    screen.blit(rotated_card, rotated_rect)
    print(angle)
    # Update the display
    pygame.display.flip()
    pygame.time.delay(30)  # Add a small delay for smoother animation

    # Limit the frame rate
    pygame.time.Clock().tick(60)