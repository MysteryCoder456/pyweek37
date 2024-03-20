from pathlib import Path
from enum import Enum

import pygame
from pygame import Vector2

ASSETS_ROOT_DIR = Path(__file__).parent / "assets"
WINDOW_SIZE = Vector2(1000, 750)
GAME_STATE_CHANGE_EVENT = pygame.USEREVENT + 99

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

    # Initial game state
    game_state = GameState.MAIN_GAME
    game_state.value.on_enter()

    while True:
        dt = clock.tick(fps) / 1000

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == GAME_STATE_CHANGE_EVENT:
                # Transition states
                game_state = event.dict["new_state"]
                game_state.on_enter()

                # Cancel state change timer
                pygame.time.set_timer(GAME_STATE_CHANGE_EVENT, 0)

            game_state.value.on_event(event)

        game_state.value.on_update(dt)
        game_state.value.on_draw(win)
