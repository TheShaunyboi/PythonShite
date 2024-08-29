import pygame
import os
import random
import sys  # Import sys for sys.exit()

# Initialize Pygame
pygame.init()

# Get the directory of the script
script_dir = os.path.dirname(__file__)

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Game Display Dimensions
display_width = 800
display_height = 600

# Create the display
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game - By Shaun')

# Clock (to control the speed of the game)
clock = pygame.time.Clock()

# Snake settings
snake_block = 10
snake_speed = 15
apple_size = 13

# Load images using the script's directory
try:
    background = pygame.image.load(os.path.join(script_dir, "background.png"))
    apple_img = pygame.image.load(os.path.join(script_dir, "apple.png"))
    
    # Resize the images
    background = pygame.transform.scale(background, (display_width, display_height))
    apple_img = pygame.transform.scale(apple_img, (apple_size, apple_size))
    
    print("Images loaded and resized successfully.")
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    display.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, white, [x[0], x[1], snake_block, snake_block])

def draw_food(foodx, foody):
    display.blit(apple_img, (foodx, foody))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3])

def gameLoop():
    print("Starting game loop...")
    game_over = False
    game_close = False

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    score = 0

    while not game_over:
        while game_close:
            display.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            print("Collision with wall detected.")
            game_close = True
        x1 += x1_change
        y1 += y1_change

        display.blit(background, (0, 0))  # Draw background

        draw_food(foodx, foody)  # Draw food (apple)
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                print("Snake collision detected.")
                game_close = True

        our_snake(snake_block, snake_list)  # Draw snake
        your_score(score)  # Display the score

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            print("Food eaten.")
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    print("Game closed.")
    sys.exit()

gameLoop()
