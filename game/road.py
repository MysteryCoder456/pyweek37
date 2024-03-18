from pathlib import Path

import pygame
from pygame.sprite import Sprite, Group
from pygame.transform import scale_by

ROAD_SPRITE_PATH = Path(__file__).parent / "assets" / "road" / "road.png"


class Road(Sprite):
    def __init__(self, win_height: float, *groups: Group) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(ROAD_SPRITE_PATH)  # type: ignore
        scale_factor = win_height / self.image.get_height() * 1.1
        self.image = scale_by(self.image, scale_factor)

        self.rect = pygame.FRect(self.image.get_rect())  # type: ignore

    def update(self, dt: float, camera_speed: float):  # type: ignore
        # Account for camera speed
        self.rect.y += camera_speed * dt  # type: ignore

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)  # type: ignore
