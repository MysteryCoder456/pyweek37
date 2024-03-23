import sys

import pygame
from pygame.freetype import Font
from pygame_gui import UI_BUTTON_PRESSED, UIManager
from pygame_gui.elements import UIButton, UILabel

from game.constants import (
    ASSETS_ROOT_DIR,
    WINDOW_SIZE,
    GAME_STATE_CHANGE_EVENT,
)
from game.game_state import GameState
from game.scene import Scene


class MainMenuScene(Scene):
    def on_enter(self) -> None:
        theme_path = ASSETS_ROOT_DIR / "ui" / "theme.json"
        self.ui = UIManager(
            (int(WINDOW_SIZE.x), int(WINDOW_SIZE.y)),
            str(theme_path),
        )

        self.title_label = UILabel(
            relative_rect=pygame.Rect(0, 100, WINDOW_SIZE.x, 100),
            text="The Boring Game",
            manager=self.ui,
            anchors={"centerx": "centerx", "top": "top"},
            object_id="#title_label",
        )

        btn_width, btn_height = 100, 60
        gap = 30
        self.play_btn = UIButton(
            relative_rect=pygame.Rect(
                0, -(gap + btn_height) / 2, btn_width, btn_height
            ),
            text="Play",
            manager=self.ui,
            anchors={"center": "center"},
        )
        self.quit_btn = UIButton(
            relative_rect=pygame.Rect(
                0, (gap + btn_height) / 2, btn_width, btn_height
            ),
            text="Quit",
            manager=self.ui,
            anchors={"center": "center"},
        )

    def on_event(self, event: pygame.Event) -> None:
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.play_btn:
                # Transition to main game scene
                event = pygame.Event(
                    GAME_STATE_CHANGE_EVENT, {"new_state": GameState.MAIN_GAME}
                )
                pygame.event.post(event)

            elif event.ui_element == self.quit_btn:
                pygame.quit()
                sys.exit()

        self.ui.process_events(event)

    def on_update(self, dt: float) -> None:
        self.ui.update(dt)

    def on_draw(self, window: pygame.Surface) -> None:
        window.fill((50, 50, 100))
        self.ui.draw_ui(window)
        pygame.display.flip()
