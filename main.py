import pygame
import sys
import random

# Initialize Pygame
pygame.init()


# Load the monkey emoji image
player_image = pygame.image.load("images.jpeg")

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 333, 600  # Adjust the dimensions to fit a vertical phone shape
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
player_image = pygame.transform.scale(player_image, (50, 50))
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 10
BG_COLOR = (255, 255, 255)  # Set background color to white
GRAVITY = 1.5
JUMP_FORCE = -15
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_INTERVAL = 60
OBSTACLE_COLOR = (255, 0, 0)  # Change obstacle color to red
#MAX = 40 #izmeniti da bude customizable

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Game")



# Player
player_x = SCREEN_WIDTH // 7
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
player_velocity_y = 0
is_jumping = False

# Obstacles
obstacles = []

# Game over flag
game_over = False

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a font for text rendering
font = pygame.font.Font(None, 36)

# Functions
def draw_player():
    screen.blit(player_image, (player_x, player_y))

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)

def generate_obstacle():
    obstacle_x = SCREEN_WIDTH
    obstacle_y = SCREEN_HEIGHT - OBSTACLE_HEIGHT - random.randint(0, player_x + JUMP_FORCE - 1) #ovde dodati----------------------------------
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

def move_obstacles():
    for obstacle in obstacles:
        obstacle.x -= OBSTACLE_SPEED

def check_collision():
    for obstacle in obstacles:
        if (player_x + PLAYER_WIDTH >= obstacle.x and player_x <= obstacle.x + OBSTACLE_WIDTH) and \
           (player_y + PLAYER_HEIGHT >= obstacle.y-10 and player_y <= obstacle.y + OBSTACLE_HEIGHT ) and \
            player_y+PLAYER_HEIGHT <= obstacle.y+OBSTACLE_HEIGHT+10 and player_y+PLAYER_HEIGHT != SCREEN_HEIGHT: return True

    return False

def die():
    for obstacle in obstacles:
        if (player_x + PLAYER_WIDTH > obstacle.x and player_x < obstacle.x + OBSTACLE_WIDTH) and \
        (player_y + PLAYER_HEIGHT < obstacle.y): return True
    return False

def show_game_over_screen():
    global game_over
    game_over = True
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Restart Game", True, (0, 0, 255))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart_rect.collidepoint(x, y):
                    # Reset the game
                    obstacles.clear()
                    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
                    player_velocity_y = 0
                    game_over = False

# Game loop
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                player_velocity_y = JUMP_FORCE
                is_jumping = True

    # Clear the screen
    screen.fill(BG_COLOR)

    if not game_over:
        # Update player position and velocity
        player_y += player_velocity_y
        player_velocity_y += GRAVITY

        # Keep the player on the ground
        if player_y > SCREEN_HEIGHT - PLAYER_HEIGHT:
            player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
            is_jumping = False
            player_velocity_y = 0

        # Generate obstacles
        if score % OBSTACLE_SPAWN_INTERVAL == 0:
            generate_obstacle()

        # Move and draw obstacles
        move_obstacles()
        draw_obstacles()

        #if die():
        #    pygame.quit()

        # Draw the player
        draw_player()        

        # Check for collisions
        if check_collision() and player_velocity_y > 0:
                player_velocity_y = JUMP_FORCE  # Bounce the player upward

            


        # Remove off-screen obstacles
        obstacles = [obstacle for obstacle in obstacles if obstacle.x > -OBSTACLE_WIDTH]

        # Increase score
        score += 1

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(30)

# Game over
pygame.quit()
sys.exit()
