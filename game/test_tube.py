import pygame
from pygame.sprite import Group, Sprite
from pygame.transform import scale_by

from game.constants import ASSETS_ROOT_DIR

TEST_TUBE_SPRITESHEET_PATH = ASSETS_ROOT_DIR / "test_tube" / "test_tube.png"


class TestTube(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)

        frame_width, frame_height = 64, 64
        frame_count = 12
        scale_factor = 1.5

        self.image = pygame.image.load(TEST_TUBE_SPRITESHEET_PATH)
        self.frames = [
            scale_by(
                self.image.subsurface(
                    (0, i * frame_height, frame_width, frame_height)
                ),
                scale_factor,
            )
            for i in range(frame_count)
        ]
        self.rect = self.frames[0].get_frect()
        self.mask = pygame.mask.from_surface(self.frames[0])

        self.animation_frame: int = 0
        self.animation_timer: float = 0
        self.animation_time: float = 1 / 8  # 8 fps

    def update(self, dt: float, camera_speed: float):  # type: ignore
        # Account for camera speed
        self.rect.y += camera_speed * dt  # type: ignore

        # Animation
        self.animation_timer += dt

        if self.animation_timer >= self.animation_time:
            self.animation_timer -= self.animation_time
            self.animation_frame = (self.animation_frame + 1) % len(
                self.frames
            )

    def draw(self, surface: pygame.Surface):
        frame = self.frames[self.animation_frame]
        surface.blit(frame, self.rect)  # type: ignore
