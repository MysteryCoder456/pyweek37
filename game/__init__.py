import os
import pygame

from game.constants import WINDOW_SIZE, GAME_STATE_CHANGE_EVENT, DATA_ROOT_DIR
from game.game_state import GameState
from game.scene import Scene
from game.scenes import MainMenuScene, MainGameScene


def main():
    pygame.init()

    # Make sure data directory exists
    os.makedirs(DATA_ROOT_DIR, exist_ok=True)

    # Initialize display
    win = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("The Boring Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    state_scene_map: dict[GameState, Scene] = {
        GameState.MAIN_MENU: MainMenuScene(),
        GameState.MAIN_GAME: MainGameScene(),
    }

    # Initial game state
    game_state = GameState.MAIN_MENU
    current_scene = state_scene_map[game_state]
    current_scene.on_enter()

    while True:
        dt = clock.tick(fps) / 1000

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == GAME_STATE_CHANGE_EVENT:
                # Transition states
                new_state: GameState = event.dict["new_state"]

                if new_state in state_scene_map:
                    game_state = new_state
                    current_scene = state_scene_map[game_state]
                    current_scene.on_enter()
                else:
                    raise Exception(
                        f"GameState.{new_state.name} has not been mapped to any scene!"
                    )

                # Cancel state change timer
                pygame.time.set_timer(GAME_STATE_CHANGE_EVENT, 0)

            else:
                current_scene.on_event(event)

        current_scene.on_update(dt)
        current_scene.on_draw(win)
