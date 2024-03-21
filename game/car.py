import pygame
from pygame.sprite import Sprite, Group
from pygame import BLEND_ALPHA_SDL2, Vector2
from pygame.transform import rotate, scale_by

from game.constants import ASSETS_ROOT_DIR

CAR_SPRITE_PATH = ASSETS_ROOT_DIR / "car" / "car.png"
CAR_SPEED_DAMPING = 0.015
CAR_ACCELERATION = 8
CAR_STEER_SPEED = 3


class Car(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)

        self.image = scale_by(pygame.image.load(CAR_SPRITE_PATH), 2)  # type: ignore
        self.rect = self.image.get_frect()  # type: ignore
        self.mask = pygame.mask.from_surface(self.image)

        self.angle: float = 0
        self.speed: float = 0

        # Got this result using some basic algebra
        self.max_speed = CAR_ACCELERATION * (1 / CAR_SPEED_DAMPING - 1)

    def update(self, dt: float, camera_speed: float):  # type: ignore
        # Calculate linear velocities from speed and angle
        velocity = Vector2()
        velocity.from_polar((self.speed, -self.angle))

        # Account for camera speed
        velocity.y += camera_speed

        self.rect = self.rect.move(velocity * dt)  # type: ignore
        self.speed *= 1 - CAR_SPEED_DAMPING

        self.mask = pygame.mask.from_surface(rotate(self.image, self.angle))  # type: ignore

    def draw(self, surface: pygame.Surface):
        img = rotate(self.image, self.angle)  # type: ignore
        pos = Vector2(self.rect.center) - Vector2(img.get_size()) / 2  # type: ignore
        surface.blit(img, pos, special_flags=BLEND_ALPHA_SDL2)
