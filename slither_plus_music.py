import pygame
import sys
import random

# Initialize
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# === Load assets ===
bg_image = pygame.image.load("grassland.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

snake_segment = pygame.image.load("snake.png")
snake_segment = pygame.transform.scale(snake_segment, (CELL_SIZE, CELL_SIZE))

apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (CELL_SIZE, CELL_SIZE))

# === Game functions ===
def random_position():
    return (
        random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    )

def draw_snake(snake):
    for segment in snake:
        screen.blit(snake_segment, segment)

def draw_apple(pos):
    screen.blit(apple_image, pos)

def draw_score(score):
    pygame.draw.rect(screen, (255, 200, 200), (0, HEIGHT - 40, WIDTH, 40))
    txt = font.render(f"score : {score}", True, (0, 0, 0))
    screen.blit(txt, (10, HEIGHT - 30))

# === Game loop ===
def game_loop(start_speed):
    snake = [(CELL_SIZE * 5, CELL_SIZE * 5)]
    direction = (CELL_SIZE, 0)
    apple = random_position()
    score = 0
    speed = start_speed

    while True:
        clock.tick(speed)
        screen.blit(bg_image, (0, 0))

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        elif keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        elif keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        elif keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake = [new_head] + snake[:-1]

        # Eat apple
        if new_head == apple:
            snake.append(snake[-1])
            apple = random_position()
            score += 1
            if score % 5 == 0:
                speed += 1  # increase speed gradually

        # Collision detection
        if new_head in snake[1:] or not (0 <= new_head[0] < WIDTH) or not (0 <= new_head[1] < HEIGHT):
            game_over_screen(score)
            return

        # Draw everything
        draw_snake(snake)
        draw_apple(apple)
        draw_score(score)
        pygame.display.flip()

# === Game over screen ===
def game_over_screen(final_score):
    screen.fill((0, 0, 0))
    msg = font.render(f"Game Over! Final Score: {final_score}", True, (255, 255, 255))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 30))
    sub = font.render("Press [R] to Restart or [Q] to Quit", True, (200, 200, 200))
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# === Speed selection screen ===
def choose_speed():
    while True:
        screen.fill((0, 0, 0))
        txt = font.render("Choose Speed: [1] Slow  [2] Normal  [3] Fast", True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 5
                elif event.key == pygame.K_2:
                    return 10
                elif event.key == pygame.K_3:
                    return 15

# === Run the game ===
if __name__ == "__main__":
    while True:
        speed = choose_speed()
        game_loop(speed)
