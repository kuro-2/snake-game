#!/usr/bin/env python3
"""
A prettier, adjustable‑speed Snake game in Pygame.
No external assets, everything rendered with primitives.
"""

import pygame
import random
import sys

# ───────────────────────── Config ────────────────────────── #

WIDTH, HEIGHT = 640, 480
CELL = 20                     # size of one grid square
GRID_W, GRID_H = WIDTH // CELL, HEIGHT // CELL

WHITE      = (245, 245, 245)
BG_COLOUR  = (230, 240, 255)
SNAKE_HEAD = ( 50, 150,  50)
SNAKE_BODY = ( 80, 200,  80)
APPLE_RED  = (220,  40,  40)
SHADOW     = (150, 150, 150, 60)   # last value = alpha

FONT_NAME  = "freesansbold.ttf"

# speed choices (frames per second)
SPEED_MAP = {1: 7, 2: 10, 3: 15, 4: 20, 5: 25}

# ───────────────────────── Helpers ───────────────────────── #
GRASS_IMG = pygame.image.load("grassland.jpg")
def draw_cell(surface, colour, pos, radius=0):
    """Draw a rounded or square cell centred on pos (grid coordinates)."""
    x, y = pos[0] * CELL, pos[1] * CELL
    rect = pygame.Rect(x, y, CELL, CELL)
    pygame.draw.rect(surface, colour, rect, border_radius=radius)

def random_cell(exclude):
    """Return a new grid cell not in *exclude* set."""
    while True:
        cell = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if cell not in exclude:
            return cell

def render_text(text, size, colour):
    font = pygame.font.Font(FONT_NAME, size)
    return font.render(text, True, colour)

# ───────────────────────── Main Game ─────────────────────── #

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slither – Better Edition")

    # ---------- Start screen ----------
    screen.fill(BG_COLOUR)
    title = render_text("SLITHER", 64, SNAKE_HEAD)
    prompt = render_text("Choose speed (1‑5)", 32, SNAKE_BODY)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//3)))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH//2, HEIGHT//3 + 80)))
    pygame.display.flip()

    fps = None
    while fps is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                n = int(event.unicode)
                if n in SPEED_MAP:
                    fps = SPEED_MAP[n]

    clock = pygame.time.Clock()

    # ---------- Initialise world ----------
    snake = [(GRID_W // 2, GRID_H // 2)]
    direction = (1, 0)  # moving right
    apple = random_cell(set(snake))
    score = 0

    running = True
    while running:
        # ----- Input -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != (0, 1):  direction = (0, -1)
                if event.key == pygame.K_DOWN  and direction != (0, -1): direction = (0,  1)
                if event.key == pygame.K_LEFT  and direction != (1, 0):  direction = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0): direction = (1,  0)

        # ----- Update snake -----
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = ((head_x + dx) % GRID_W, (head_y + dy) % GRID_H)  # wrap‑around walls

        # collision with self → game over
        if new_head in snake:
            running = False
            break

        snake.insert(0, new_head)

        if new_head == apple:
            score += 1
            apple = random_cell(set(snake))
        else:
            snake.pop()

        # ----- Draw frame -----
        screen.fill(BG_COLOUR)

        # Drop shadow for apple
        apple_px = (apple[0] * CELL + CELL // 2, apple[1] * CELL + CELL // 2)
        shadow = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        pygame.draw.circle(shadow, SHADOW, (CELL//2, CELL//2 + 3), CELL//2)
        screen.blit(shadow, shadow.get_rect(center=apple_px))

        # Apple
        pygame.draw.circle(screen, APPLE_RED, apple_px, CELL // 2)

        # Snake segments
        for i, cell in enumerate(snake):
            col = SNAKE_HEAD if i == 0 else SNAKE_BODY
            draw_cell(screen, col, cell, radius=6)

        # Score
        score_surf = render_text(f"Score: {score}", 24, (0, 0, 0))
        screen.blit(score_surf, (10, 10))

        pygame.display.update()
        clock.tick(fps)

    # ---------- Game over ----------
    screen.fill(BG_COLOUR)
    over = render_text("GAME OVER", 64, APPLE_RED)
    final = render_text(f"Final score: {score}", 32, (50, 50, 50))
    info = render_text("Press any key to quit", 24, (80, 80, 80))
    screen.blit(over,  over.get_rect(center=(WIDTH//2, HEIGHT//3)))
    screen.blit(final, final.get_rect(center=(WIDTH//2, HEIGHT//3 + 70)))
    screen.blit(info,  info.get_rect(center=(WIDTH//2, HEIGHT//3 + 120)))
    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.QUIT):
                wait = False
    pygame.quit()


if __name__ == "__main__":
    main()
