from pathlib import Path

import pygame
from pygame import Vector2, BLEND_ALPHA_SDL2
from pygame.freetype import Font

from game.car import (
    CAR_ACCELERATION,
    CAR_STEER_SPEED,
    Car,
)


def main():
    pygame.init()

    # Initialize display
    win_size = Vector2(1000, 750)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("The Boring Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    # Initialize fonts
    font_path = Path(__file__).parent / "assets" / "fonts" / "MPLUS1Code.ttf"
    font = Font(font_path)

    # Initialize game objects
    car = Car()

    while True:
        dt = clock.tick(fps) / 1000

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()

        # Acceleration
        if keys[pygame.K_w]:
            car.speed += CAR_ACCELERATION
        elif keys[pygame.K_s]:
            car.speed -= CAR_ACCELERATION * 0.5

        # Steering
        steer = int(keys[pygame.K_a]) - int(keys[pygame.K_d])
        car.angle += steer * car.speed / car.max_speed * CAR_STEER_SPEED

        # Update
        car.update(dt)

        # Draw
        win.fill((50, 50, 100))

        car.draw(win)

        text, text_rect = font.render("Hello, World!", "white", size=46)
        win.blit(
            text,
            (
                (win_size.x - text_rect.width) / 2,
                (win_size.y - text_rect.height) / 2,
            ),
            special_flags=BLEND_ALPHA_SDL2,
        )

        pygame.display.flip()
