from pathlib import Path

import pygame
from pygame.sprite import Sprite, Group
from pygame import BLEND_ALPHA_SDL2, Vector2
from pygame.transform import rotate

CAR_SPRITE_PATH = Path(__file__).parent / "assets" / "car" / "car.png"
CAR_SPEED_DAMPING = 0.02
CAR_ACCELERATION = 8
CAR_STEER_SPEED = 3


class Car(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load(CAR_SPRITE_PATH)
        self.rect = pygame.FRect(self.image.get_rect())

        self.angle: float = 0
        self.speed: float = 0

        # Got this result using some basic algebra
        self.max_speed = CAR_ACCELERATION * (1 / CAR_SPEED_DAMPING - 1)

    def update(self, dt: float):  # type: ignore
        velocity = Vector2()
        velocity.from_polar((self.speed, -self.angle))
        self.rect = self.rect.move(velocity * dt)  # type: ignore
        self.speed *= 1 - CAR_SPEED_DAMPING

    def draw(self, surface: pygame.Surface):
        img = rotate(self.image, self.angle)  # type: ignore
        pos = Vector2(self.rect.center) - Vector2(img.get_size()) / 2  # type: ignore
        surface.blit(img, pos, special_flags=BLEND_ALPHA_SDL2)
