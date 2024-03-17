import pygame
from pygame import Vector2


def main():
    # Initialize display
    win_size = Vector2(800, 600)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("Tube Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(fps) / 1000

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update
        # ...

        # Draw
        win.fill(50)
        pygame.display.flip()
