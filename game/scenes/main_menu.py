import pygame
from pygame.freetype import Font
from pygame_gui import UI_BUTTON_PRESSED, UIManager
from pygame_gui.elements import UIButton

from game.constants import (
    ASSETS_ROOT_DIR,
    WINDOW_SIZE,
    GAME_STATE_CHANGE_EVENT,
)
from game.game_state import GameState
from game.scene import Scene


class MainMenuScene(Scene):
    def on_enter(self) -> None:
        self.ui = UIManager((int(WINDOW_SIZE.x), int(WINDOW_SIZE.y)))

        font_path = ASSETS_ROOT_DIR / "fonts" / "MPLUS1Code.ttf"
        self.font = Font(font_path)

        play_btn_rect = pygame.Rect(0, 0, 100, 50)
        play_btn_rect.center = WINDOW_SIZE / 2
        self.play_btn = UIButton(
            relative_rect=play_btn_rect,
            text="PLAY",
            manager=self.ui,
        )

    def on_event(self, event: pygame.Event) -> None:
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.play_btn:
                # Transition to main game scene
                event = pygame.Event(
                    GAME_STATE_CHANGE_EVENT, {"new_state": GameState.MAIN_GAME}
                )
                pygame.event.post(event)

        self.ui.process_events(event)

    def on_update(self, dt: float) -> None:
        self.ui.update(dt)

    def on_draw(self, window: pygame.Surface) -> None:
        window.fill((50, 50, 100))
        self.ui.draw_ui(window)
        pygame.display.flip()
