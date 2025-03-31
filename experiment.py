import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Game display settings
display = (800, 600)
#icon = "Project_Sem_2\\pong.png"

# Player settings
player1_speed = 0.5
player2_speed = 0.5
player_height = 90
player_width = 8

# Font for displaying scores and messages
font = pygame.font.Font('freesansbold.ttf', 50)
    
# Scores for both players
score1 = 0
score2 = 0

# Game state variables
running2 = True
player_xdisplacement = 3

# Ball settings
ball_radius = 7
ball_speed = 0.4

# Function to initialize or reset the game state
def start_game():
    global ball_x, ball_y, player1_x, player1_y, player2_x, player2_y, ball_speedx, ball_speedy
    
    # Ball starts at the center of the screen
    ball_x = display[0] / 2
    ball_y = display[1] / 2
    
    # Players' paddles initial positions
    player1_x, player1_y = (player_xdisplacement, display[1] / 2 - player_height / 2)
    player2_x, player2_y = (display[0] - player_width - player_xdisplacement, display[1] / 2 - player_height / 2)
    
    # Randomize the ball's starting angle while ensuring it isn't too vertical or horizontal
    angle_list = list(filter(lambda x: math.fabs(90 - x) >= 60, list(range(0, 180))))
    start_angle = random.choice(angle_list)
    
    # Calculate initial ball speed in x and y directions based on the angle
    ball_speedx = ball_speed * math.cos(start_angle * math.pi / 180)
    ball_speedy = ball_speed * math.sin(start_angle * math.pi / 180)

# Start the game for the first time
start = True
start_game()

# Function to draw Player 2's paddle on the screen
def player2(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, player_width, player_height))

# Function to draw the ball on the screen
def ball(x, y):
    pygame.draw.circle(screen, (0, 255, 255), (x, y), radius=ball_radius)

# Function to draw Player 1's paddle on the screen
def player1(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, player_width, player_height))

# Load game icon and set up the display window
#icon = pygame.image.load(icon)
screen = pygame.display.set_mode(display)
pygame.display.set_caption('Pong')
#pygame.display.set_icon(icon)

# Main game loop variables
running = True
moving1_x = moving1_y = moving2_x = moving2_y = False

while running:
    # Fill the screen with black to clear previous frames
    screen.fill((0, 0, 0))
    
    # Check if the game has ended; if so, pause and exit after a delay
    if running2 == False:
        time.sleep(4)
        running = False
    
    # Event handling loop for user input and quitting the game
    for event in pygame.event.get():
        # Handle quit event
        if event.type == pygame.QUIT:
            running = False
        
        # Handle keyboard input for paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                moving2_x = True
                speed2 = -player2_speed
            if event.key == pygame.K_DOWN:
                moving2_y = True
                speed2 = player2_speed
            if event.key == pygame.K_w:
                moving1_x = True
                speed1 = -player1_speed
            if event.key == pygame.K_s:
                moving1_y = True
                speed1 = player1_speed
        
        # Handle key releases to stop paddle movement when keys are released
        if event.type == pygame.KEYUP:
            moving2_x = False if event.key == pygame.K_UP else moving2_x
            moving2_y = False if event.key == pygame.K_DOWN else moving2_y
            moving1_x = False if event.key == pygame.K_w else moving1_x
            moving1_y = False if event.key == pygame.K_s else moving1_y
    
    # Restart the game after a point is scored or at the beginning of the game loop
    if start == True:
        start_game()
        time.sleep(1)
        start = False

    # Player 2 movement mechanics (up and down within screen bounds)
    if moving2_x == True or moving2_y == True:
        if (player2_y + speed2) <= (display[1] - player_height) and (player2_y + speed2) >= 0:
            player2_y += speed2
            
        elif player2_y >= (display[1] - player_height):
            player2_y = display[1] - player_height
        
        elif player2_y <= 0:
            player2_y = 0
    
    # Player 1 movement mechanics (up and down within screen bounds)
    if moving1_x == True or moving1_y == True:
        if player1_y + speed1 <= (display[1] - player_height) and player1_y + speed1 >= (0):
            player1_y += speed1
            
        elif player1_y >= (display[1] - player_height):
            player1_y = display[1] - player_height
        
        elif player1_y <= (0):
            player1_y = 0   
    
    # Ball collision with Player 1's paddle 
    if (int(ball_x - ball_radius) == player_xdisplacement + player_width 
        and player1_y <= ball_y <= player1_y + player_height):
        ball_speedx = -ball_speedx
    
    # Ball collision with Player 2's paddle 
    if int(ball_x + ball_radius) == display[0] - (player_xdisplacement + player_width) \
       and player2_y <= ball_y <= player2_y + player_height:
        ball_speedx = -ball_speedx
    
    # Ball goes past Player 2's side; Player 1 scores a point 
    if ball_x >= display[0] - ball_radius: 
        ball_speedx = ball_speedy = 0 
        start = True 
        score1 += 1 
        time.sleep(0.5)

    # Ball goes past Player 1's side; Player 2 scores a point 
    if ball_x <= ball_radius: 
        ball_speedx = ball_speedy = 0 
        start = True 
        time.sleep(0.5)
        score2 += 1

    # Ball hits top or bottom of the screen; reverse y direction
    if ball_y >= display[1] - ball_radius or ball_y <= ball_radius:
        ball_speedy = -ball_speedy

    # Check for game over conditions
    if score1 == 5:
        start = False
        screen.blit(font.render('PLAYER 1 WON', True, (255, 0, 0)), (display[0] / 2 - 170, display[1] / 2 - 25))
        running2 = False

    if score2 == 5:
        start = False
        screen.blit(font.render('PLAYER 2 WON', True, (255, 0, 0)), (display[0] / 2, display[1] / 2))
        running2 = False

    # Update ball position
    ball_x += ball_speedx
    ball_y += ball_speedy

    # Render scores
    score1_rendered = font.render(str(score1), True, (255, 255, 255))
    score2_rendered = font.render(str(score2), True, (255, 255, 255))
    screen.blit(score1_rendered, (display[0] / 2 - 62.5, 10))
    screen.blit(score2_rendered, (display[0] / 2 + 37.5, 10))

    # Draw game elements
    ball(ball_x, ball_y)
    player2(player2_x, player2_y)
    player1(player1_x, player1_y)

    # Update the display
    pygame.display.update()
