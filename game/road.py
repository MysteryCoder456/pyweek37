from pathlib import Path

import pygame
from pygame.sprite import Sprite, Group

ROAD_SPRITE_PATH = Path(__file__).parent / "assets" / "road" / "road.png"


class Road(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(ROAD_SPRITE_PATH)  # type: ignore
        self.rect = self.image.get_rect()  # type: ignore

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)  # type: ignore
