import pygame

from game.scene import Scene


class MainMenuScene(Scene):
    def on_enter(self) -> None:
        return super().on_enter()

    def on_event(self, event: pygame.Event) -> None:
        return super().on_event(event)

    def on_update(self, dt: float) -> None:
        return super().on_update(dt)

    def on_draw(self, window: pygame.Surface) -> None:
        return super().on_draw(window)
