import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
SNAKE_SIZE = 20
SNAKE_SPEED = 15
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slither")

# Initialize Snake
snake = [(100, 50)]
snake_direction = 'RIGHT'

# Initialize Food
food = (random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
        random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # Move the Snake
    if snake_direction == 'UP':
        new_head = (snake[0][0], snake[0][1] - SNAKE_SIZE)
    elif snake_direction == 'DOWN':
        new_head = (snake[0][0], snake[0][1] + SNAKE_SIZE)
    elif snake_direction == 'LEFT':
        new_head = (snake[0][0] - SNAKE_SIZE, snake[0][1])
    else:
        new_head = (snake[0][0] + SNAKE_SIZE, snake[0][1])

    snake.insert(0, new_head)

    # Check for collisions with food
    if snake[0] == food:
        food = (random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)
    else:
        snake.pop()

    # Check for collisions with walls
    if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
        snake[0][1] < 0 or snake[0][1] >= HEIGHT):
        running = False

    # Check for collisions with itself
    for segment in snake[1:]:
        if snake[0] == segment:
            running = False

    # Clear the screen
    window.fill(WHITE)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(window, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    # Draw the food
    pygame.draw.rect(window, RED, (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.display.update()

    # Control game speed
    pygame.time.Clock().tick(SNAKE_SPEED)

# Quit Pygame
pygame.quit()
