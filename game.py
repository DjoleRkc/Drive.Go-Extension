import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()


# Load the monkey emoji image
global player_image
player_image = pygame.image.load("trci1.png")
player_images = [pygame.image.load("trci1.png"), pygame.image.load("trci2.png"), pygame.image.load("trci3.png"), pygame.image.load("trci4.png")]
obstacle_image = pygame.image.load('stepenik.png')
kupon_images = [pygame.image.load('kafe.png'), pygame.image.load('kartica.png'),pygame.image.load('kroasan.png'),pygame.image.load('sendvici.png'),\
                pygame.image.load('tocenje.png'),pygame.image.load('ulja.png')]
global curr_imm
global dir_imm
curr_imm = 0
dir_imm = 1
obstacle_image = pygame.image.load('stepenik.png')
# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600  # Adjust the dimensions to fit a vertical phone shape
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

player_images[0] = pygame.transform.scale(player_images[0], (PLAYER_WIDTH, PLAYER_HEIGHT))
player_images[1] = pygame.transform.scale(player_images[1], (PLAYER_WIDTH, PLAYER_HEIGHT+20))
player_images[2] = pygame.transform.scale(player_images[2], (PLAYER_WIDTH, PLAYER_HEIGHT+20))
player_images[3] = pygame.transform.scale(player_images[3], (PLAYER_WIDTH, PLAYER_HEIGHT+20))

OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 80, 20
KUPON_WIDTH, KUPON_HEIGHT = 50, 35
obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
kupon_images = [ pygame.transform.scale(imm, (KUPON_WIDTH, KUPON_HEIGHT)) for imm in kupon_images ]

BG_COLOR = (255, 255, 255)  # Set background color to white
GRAVITY = 2
JUMP_FORCE = -25
OBSTACLE_SPEED = 8
OBSTACLE_SPAWN_INTERVAL = 20
OBSTACLE_COLOR = (255, 0, 0)  # Change obstacle color to red
global last_generated_obstacle
last_generated_obstacle = None

firstWalking = True
fuelFilled = False

#creating banner
text_container = pygame.Surface((SCREEN_WIDTH, 100))
text_container.fill((140, 156, 175))  # Black background for text container
scroll_text = ["NIS poseduje preko 400 benzinskih stanica u Srbiji i regionu",\
               "Drive Cafe nudi veliku selekciju svežih peciva i kvalitetnih italijanskih kafa", \
                "Mesečno se natoči oko 50 000 000 litara goriva na NIS-ovim benzinskim stanicama",\
                "SA NAMA NA PUTU aplikacija ima preko 1 200 000 korisnika", \
                "Drive.Go aplikacija ima preko 140 000 korisnika", \
                "NIS poseduje benzinske stanice u Srbiji, BiH, Bugarskoj i Rumuniji", \
                "Prosečan broj transakcija na NISovim pumpama je oko 80 000 dnevno", \
                "NIS u svojoj selekciji ima preko 10 naftnih derivata", \
                "Drive Caffe dnevno proda preko 12 000 šoljica kafe", \
                "NIS je nedavno otvorio prvu bezkontaktnu pumpu na lokaciji Ušće", \
                "Neke od NISovih partnerska firmi su Gigatron, Umbro i Vozzi", \
                "NIS poseduje 45+ naftnih i gasnih polja u Srbiji sa preko 900+ bušotina", \
                "Kupovinom u partnerskim firmama poput Gigatrona i Vozzi ostvarujete bodove koje možete potrošiti na NIS pumpama", \
                "NIS nudi GDrive premium gorivo koje obezbeđuje profesionalnu zaštitu, efikasniji rad i poboljšanje performanse motora tvog automobila", \
                "Jedna od značajnih delatnosti NIS-a je snabdevanje vazduhoplova avio-gorivom koje kompanija proizvodi u Rafineriji nafte Pančevo", \
                "Drive.Go je prva aplikacija u regionu koja nudi opciju plaćanja bez odlaska na kasu na benzinskoj stanici", \
                "NIS nudi loyalty program koji omogućava popuste na benzinskim stanicama, sakupljanje i korišćenje bonus poena na benzinskim stanicama i u partnerskim kompanijama", \
                "Bitumen se proizvodi u rafineriji Pančevo, a otprema se odvija 24 sata dnevno, 7 dana u nedelji"]
scroll_text_x = SCREEN_WIDTH // 2
scroll_text_y = 40  # Pushed to the top
text_ind = 0

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, 700))
pygame.display.set_caption("Drive.Go")
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player
player_x = SCREEN_WIDTH // 7
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
player_velocity_y = 0
is_jumping = False

# Obstacles
obstacles = []
coupons = []
coupon_images = []
collected_coupons = []

# Game over flag
global game_over
game_over = False

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a font for text rendering
font = pygame.font.Font(None, 36)

#button properties
button_width, button_height = 200, 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2 + 50
button_color = (0, 0, 255)
button_text = font.render("Restart Game", True, (255, 255, 255))
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)



# Functions
def draw_player():
    screen.blit(player_image, (player_x, player_y))

def draw_obstacles():
    for obstacle in obstacles:
        #pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))
    for i in range(len(coupons)):
        screen.blit(coupon_images[i], (coupons[i].x, coupons[i].y))


def generate_obstacle():
    global last_generated_obstacle
    obstacle_x = SCREEN_WIDTH

    if last_generated_obstacle:
        tmp = SCREEN_HEIGHT
        while(tmp > SCREEN_HEIGHT - OBSTACLE_HEIGHT or tmp < 150):
            tmp = last_generated_obstacle.y - OBSTACLE_HEIGHT - random.randint(-PLAYER_HEIGHT - 30, PLAYER_HEIGHT + 30) 
    else:
        tmp = SCREEN_HEIGHT - OBSTACLE_HEIGHT - random.randint(0, PLAYER_HEIGHT + 30)
    
    obstacle_y = tmp
    last_generated_obstacle = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacles.append(pygame.Rect(obstacle_x - (OBSTACLE_WIDTH/2) + (KUPON_WIDTH/2), obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    #deo za kupone:

    if random.randint(1, 100) <= 25:
        #print('milionerea')
        coupons.append(pygame.Rect(obstacle_x, obstacle_y - KUPON_HEIGHT - 10, KUPON_WIDTH, KUPON_HEIGHT))
        coupon_images.append(kupon_images[random.randint (0, len(kupon_images) - 1)])


def move_obstacles():
    for obstacle in obstacles:
        obstacle.x -= OBSTACLE_SPEED
    for coupon in coupons:
        coupon.x -= OBSTACLE_SPEED

def move_player():
    global player_image
    global curr_imm
    global dir_imm
    if score % 6 == 0:
        player_image = player_images[curr_imm + dir_imm]
        curr_imm = curr_imm + dir_imm
        if curr_imm == len(player_images) - 1 : dir_imm = -1
        elif curr_imm == 0 : dir_imm = 1

def check_collision():
    for obstacle in obstacles:
        if (player_x + PLAYER_WIDTH >= obstacle.x and player_x <= obstacle.x + OBSTACLE_WIDTH) and \
           (player_y + PLAYER_HEIGHT >= obstacle.y-10 and player_y <= obstacle.y + OBSTACLE_HEIGHT ) and \
            player_y + PLAYER_HEIGHT <= obstacle.y+OBSTACLE_HEIGHT+10 and player_y+PLAYER_HEIGHT != SCREEN_HEIGHT: return obstacle

    return False

def die():
    for obstacle in obstacles:
        if (player_x + PLAYER_WIDTH > obstacle.x and player_x < obstacle.x + OBSTACLE_WIDTH) and \
        (player_y + PLAYER_HEIGHT < obstacle.y): return True
    return False

def show_game_over_screen():
    global game_over
    global firstWalking
    global last_generated_obstacle
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
                    coupons.clear()
                    coupon_images.clear()
                    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
                    player_velocity_y = 0
                    game_over = False
                    firstWalking = True
                    last_generated_obstacle = None
                    
def kuponi():
    # Constants
    WIDTH, HEIGHT = 800, 600
    GRID_COLS, GRID_ROWS = 3, 2
    MARGIN = 5  # Margin between cells
    CELL_WIDTH = (WIDTH - (GRID_COLS + 1) * MARGIN) // GRID_COLS
    CELL_HEIGHT = (HEIGHT - (GRID_ROWS + 1) * MARGIN) // GRID_ROWS
    LINE_COLOR = (255, 0, 0)
    BORDER_THICKNESS = 2
    FONT_COLOR = (255, 255, 255)  # White text color
    FONT_SIZE = 40  # Adjust the font size as needed

    # Calculate the size of the image placement area within each cell (1/4 of the cell)
    IMAGE_AREA_SIZE = (CELL_WIDTH // 2, CELL_HEIGHT // 2)

    # Calculate the offset to center the image within the 1/4 placement area
    OFFSET_X = (CELL_WIDTH - IMAGE_AREA_SIZE[0]) // 2
    OFFSET_Y = (CELL_HEIGHT - IMAGE_AREA_SIZE[1]) // 2

    #---------------------
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sakupili ste tokene")

    # Load and scale the background image
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Create a font object for the text
    font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

    # Define the text and render it
    text1 = f"Sakupili ste {len(collected_coupons)} kupona!"
    text2 = "NIS"
    text3 = "Drive.Go"
    text4 = "Sakupili ste dovoljno kupona za greb-greb!"
    text1_rendered = font.render(text1, True, (255, 255, 255))  # White text
    text2_rendered = font.render(text2, True, (255, 255, 255))  # White text
    text3_rendered = font.render(text3, True, (255, 255, 255))  # White text
    text4_rendered = font.render(text4, True, (255, 255, 255))  # White text

    # Calculate the position to center the text
    text1_x = (WIDTH - text1_rendered.get_width()) // 2
    text2_x = (WIDTH - text2_rendered.get_width()) // 2
    text3_x = (WIDTH - text3_rendered.get_width()) // 2
    text4_x = (WIDTH - text4_rendered.get_width()) // 2
    text_y = 100  # Adjust this value to control the vertical position of the text

    # Load and scale the image
    image = pygame.image.load("photo.png")
    image = pygame.transform.scale(image, (200, 200))  # Adjust the size as needed
    image_x = (WIDTH - image.get_width()) // 2
    image_y = text_y + 200  # Adjust the vertical position below "Drive.Go"

    screen.blit(background_image, (0, 0))

    # Draw the centered text
    screen.blit(text1_rendered, (text1_x, text_y))
    screen.blit(text2_rendered, (text2_x, text_y + 50))  # Adjust vertical spacing as needed
    screen.blit(text3_rendered, (text3_x, text_y + 100))  # Adjust vertical spacing as needed
    if (len(collected_coupons) > 3):
        screen.blit(text4_rendered, (text4_x, text_y + 150))  # Adjust vertical spacing as needed


    # Draw the image
    screen.blit(image, (image_x, image_y))

    pygame.display.flip()  # Update the display



    time.sleep(3)

    if (len(collected_coupons) <= 3):
        pygame.quit()
        sys.exit()
    #  --------------------------------------------------------------

    # Create a Pygame screen with the specified dimensions
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kupon Grid")

    # Load a list of random images (adjust the image paths as needed)
    kupon_paths = [
        "kafe1.png",
        "kartica1.png",
        "kroasan1.png",
        "sendvici1.png",
        "tocenje1.png",
        "ulja1.png",
    ]
    random.shuffle(kupon_paths)

    # Create the grid to store images for each cell
    grid = [['white' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    # Choose a random cell to be flippable
    flippable_row = random.randint(0, GRID_ROWS - 1)
    flippable_col = random.randint(0, GRID_COLS - 1)
    grid[flippable_row][flippable_col] = 'white'

    # Define a font for the 'drive.go' and 'NIS' text
    font = pygame.font.Font(None, FONT_SIZE)

    # Load and scale the background image
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (CELL_WIDTH, CELL_HEIGHT))

    # Main game loop
    game_over = False
    flippable_clicked = False
    selected_coupon = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and not flippable_clicked and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - MARGIN) // (CELL_WIDTH + MARGIN)
                row = (y - MARGIN) // (CELL_HEIGHT + MARGIN)

                if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS and grid[row][col] == 'white':
                    # Reveal the kupon image when the flippable cell is clicked
                    grid[row][col] = kupon_paths.pop()
                    selected_coupon = grid[row][col]
                    flippable_clicked = True
                    game_over = True
                    

                    # Check if all images have been revealed
                    if not kupon_paths:
                        game_over = True

        # Clear the screen
        screen.fill((0, 0, 0))  # Black background color

        #dod

        # Draw the grid lines and cell borders
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                cell_x = j * (CELL_WIDTH + MARGIN) + MARGIN
                cell_y = i * (CELL_HEIGHT + MARGIN) + MARGIN

                # Draw the background rectangle for each cell
                pygame.draw.rect(screen, (255, 255, 0), (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))

                # Draw the cell border
                pygame.draw.rect(screen, LINE_COLOR, (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT), BORDER_THICKNESS)

                # Display the background image within each cell
                screen.blit(background_image, (cell_x, cell_y))

        # Draw images in the cells, centered within the 1/4 placement area
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                if grid[i][j] != 'white':
                    # Load and display the kupon image
                    image = pygame.image.load(grid[i][j])
                    image = pygame.transform.scale(image, (CELL_WIDTH - 20, CELL_HEIGHT - 20))
                    image_rect = image.get_rect()
                    image_rect.center = (j * (CELL_WIDTH + MARGIN) + CELL_WIDTH // 2 + MARGIN,
                                        i * (CELL_HEIGHT + MARGIN) + CELL_HEIGHT // 2 + MARGIN)
                    screen.blit(image, image_rect)

                # Add 'drive.go' text at the top-left corner of each cell
                drive_go_text = font.render('Drive.Go', True, FONT_COLOR)
                drive_go_text_rect = drive_go_text.get_rect()
                drive_go_text_rect.topleft = (j * (CELL_WIDTH + MARGIN) + MARGIN + BORDER_THICKNESS,
                                            i * (CELL_HEIGHT + MARGIN) + MARGIN + BORDER_THICKNESS)
                screen.blit(drive_go_text, drive_go_text_rect)

                # Add 'NIS' text in the top-right corner of each cell
                nis_text = font.render('NIS', True, FONT_COLOR)
                nis_text_rect = nis_text.get_rect()
                nis_text_rect.topright = (j * (CELL_WIDTH + MARGIN) + CELL_WIDTH - MARGIN - BORDER_THICKNESS,
                                        i * (CELL_HEIGHT + MARGIN) + MARGIN + BORDER_THICKNESS)
                screen.blit(nis_text, nis_text_rect)

        # Update the display
        pygame.display.flip()

    
        if game_over:
            time.sleep(2)

            #---------------------------------------
            pygame.display.set_caption("Osvojili ste sledeći kupon")

            # Load and scale the background image
            background_image = pygame.image.load("background.png")
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

            # Load and scale the image to be displayed above the text
            above_text_image = pygame.image.load("photo.png")
            above_text_image = pygame.transform.scale(above_text_image, (200, 200))  # Adjust the size as needed
            above_text_image_x = (WIDTH - above_text_image.get_width()) // 2
            above_text_image_y = 100  # Adjust the vertical position above the text

            # Create a font object for the text
            font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

            # Define the text and render it
            text = "Dobili ste dodatni kupon!"
            text_rendered = font.render(text, True, (255, 255, 255))  # White text

            # Calculate the position to center the text
            text_x = (WIDTH - text_rendered.get_width()) // 2
            text_y = above_text_image_y + above_text_image.get_height() + 20

            # Load and scale the image
            image = pygame.image.load(selected_coupon)
            image = pygame.transform.scale(image, (200, 200))  # Adjust the size as needed
            image_x = (WIDTH - image.get_width()) // 2
            image_y = text_y + text_rendered.get_height() + 20  # Adjust the vertical position below the text

            screen.blit(background_image, (0, 0))

    # Draw the image above the text
            screen.blit(above_text_image, (above_text_image_x, above_text_image_y))

            # Draw the centered text
            screen.blit(text_rendered, (text_x, text_y))

            # Draw the image below the text
            screen.blit(image, (image_x, image_y))

            pygame.display.flip()  # Update the display

            time.sleep(3)
            #------------------------------------------

            

            pygame.quit()
            sys.exit()



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
                firstWalking = False
            elif event.key == pygame.K_ESCAPE:
                fuelFilled = True

    # Clear the screen
    #screen.fill(BG_COLOR)
    screen.blit(background_image, (0, 0))

    if not game_over:

        if fuelFilled:
            screen.blit(font.render("ZAVRSENO TOCENJE", True, (255, 255, 255)) , (370, 20))

        screen.blit(text_container, (0, 600))

        if score % 100 == 0 : 
            text_container.fill((140, 156, 175)) 
            text_surface = font.render(scroll_text[text_ind], True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center = (scroll_text_x, scroll_text_y))
            size = text_surface.get_size()
            pygame.transform.scale(text_surface, (500, 20))
            text_container.blit(text_surface, text_rect)
            text_ind = (text_ind + 1) % len(scroll_text)

        move_player()
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
            #if random.randint(1, 100) <= 50:
            generate_obstacle()

        # Move and draw obstacles
        move_obstacles()
        draw_obstacles()

        #if die():
        #    pygame.quit()

        # Draw the player
        draw_player()        

        # Check for collisions
        #if check_collision() and player_velocity_y > 0:
        #    #player_velocity_y = JUMP_FORCE  # Bounce the player upward
        #    pass

        #KOLIZIJA SA STEPENICAMA
        obj = check_collision()
        if(obj):
            player_y = obj.y - PLAYER_HEIGHT
            player_velocity_y = 0
            is_jumping = False
        if obj == False and is_jumping == False:
            player_velocity_y += 1.5

        #KOLIZIJA SA KUPONIMA

        for coupon in coupons:
            if (player_x + PLAYER_WIDTH >= coupon.x and player_x <= coupon.x + KUPON_WIDTH) and \
            (player_y + PLAYER_HEIGHT >= coupon.y-10 and player_y <= coupon.y + KUPON_HEIGHT ):
                collected_coupons.append(coupon)
                coupon_images.pop(coupons.index(coupon))
                coupons.remove(coupon)



        if(player_y + PLAYER_HEIGHT == SCREEN_HEIGHT and firstWalking == False):
            if(fuelFilled): #idi na kupone
                kuponi()
            else:#retry
                show_game_over_screen()

            
        # Remove off-screen obstacles
        obstacles = [obstacle for obstacle in obstacles if obstacle.x > -OBSTACLE_WIDTH]
        coupons = [coupon for coupon in coupons if coupon.x > -KUPON_WIDTH]
        # Increase score
        score += 1

    # Update the display
    pygame.display.flip() #ovde uklonjen .dispay()

    # Cap the frame rate
    clock.tick(30)

# Game over
pygame.quit()
sys.exit()
