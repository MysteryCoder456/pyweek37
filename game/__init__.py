from pathlib import Path

import pygame
from pygame import Vector2
from pygame.freetype import Font


def main():
    pygame.init()

    # Initialize display
    win_size = Vector2(800, 600)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("Tube Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    # Initialize fonts
    font_path = Path(__file__).parent / "assets" / "fonts" / "MPLUS1Code.ttf"
    font = Font(font_path)

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

        text, text_rect = font.render("Hello, World!", "white", size=46)
        win.blit(
            text,
            (
                (win_size.x - text_rect.width) / 2,
                (win_size.y - text_rect.height) / 2,
            ),
        )

        pygame.display.flip()
