import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Persistent Animation Example')

# List to hold the state of circles
circles = []

# Function to perform animation
def animate_circle(start_pos, initial_radius, duration):
    clock = pygame.time.Clock()
    frames = duration * 60  # Assuming 60 frames per second

    for frame in range(frames):
        # Calculate the current radius for the animation effect
        current_radius = initial_radius + (frame * 2)  # Expand the radius

        # Draw all previous circles
        screen.fill((135, 206, 250))  # Clear the screen with background color
        for pos, radius in circles:
            pygame.draw.circle(screen, (0, 255, 0), pos, radius)  # Green circles

        # Draw the current expanding circle
        pygame.draw.circle(screen, (0, 255, 0), start_pos, current_radius)

        # Draw static graphics
        pygame.draw.rect(screen, (255, 0, 0), (150, 100, 200, 150))  # Red rectangle

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)  # Limit to 60 frames per second

    # After the animation, add the circle to the list
    circles.append((start_pos, current_radius))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # Press 'A' to trigger the animation
                animate_circle((400, 300), 20, 2)  # Start position, initial radius, duration in seconds

    # Clear the screen and draw static elements if needed
    screen.fill((135, 206, 250))  # Background color
    pygame.draw.rect(screen, (255, 0, 0), (150, 100, 200, 150))  # Draw red rectangle

    # Draw all previously animated circles
    for pos, radius in circles:
        pygame.draw.circle(screen, (0, 255, 0), pos, radius)  # Green circles

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()