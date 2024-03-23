import pygame
from pygame.sprite import Group, Sprite
from pygame.transform import scale_by

from game.constants import ASSETS_ROOT_DIR

HEART_SPRITE_PATH = ASSETS_ROOT_DIR / "heart" / "heart.png"


class Heart(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)

        scale_factor = 4

        self.image = scale_by(
            pygame.image.load(HEART_SPRITE_PATH), scale_factor
        )
        self.rect = self.image.get_frect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float, camera_speed: float):  # type: ignore
        # Account for camera speed
        self.rect.y += camera_speed * dt  # type: ignore

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)  # type: ignore
