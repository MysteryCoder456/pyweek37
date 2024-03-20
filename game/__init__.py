from pathlib import Path
from enum import Enum

import pygame
from pygame import Vector2

ASSETS_ROOT_DIR = Path(__file__).parent / "assets"
WINDOW_SIZE = Vector2(1000, 750)

# Importing this here to avoid cyclic imports
from game.scenes import MainGameScene  # noqa: E402


class GameState(Enum):
    MAIN_GAME = MainGameScene()


def main():
    pygame.init()

    # Initialize display
    win = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("The Boring Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    game_state = GameState.MAIN_GAME

    # enter
    game_state.value.on_enter()

    while True:
        dt = clock.tick(fps) / 1000

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            game_state.value.on_event(event)

        # update
        game_state.value.on_update(dt)

        # Draw
        game_state.value.on_draw(win)
