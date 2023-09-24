import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200
FONT_SIZE = 20

# Colors
WHITE = (255, 255, 255)

# Text to display
text = "NECU DA UCIM OCU DA SE BIJEM"

# Create the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

running = True
angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Calculate the position for each character
    for i, char in enumerate(text):
        char_surface = font.render(char, True, (0, 0, 0))
        char_rect = char_surface.get_rect()
        char_angle = angle + (i / len(text)) * 2 * math.pi
        char_x = CENTER[0] + RADIUS * math.cos(char_angle) - char_rect.width / 2
        char_y = CENTER[1] + RADIUS * math.sin(char_angle) - char_rect.height / 2
        screen.blit(char_surface, (char_x, char_y))

    pygame.display.flip()
    angle += 0.0001  # Adjust the speed of rotation as needed

pygame.quit()
