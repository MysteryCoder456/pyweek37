from pathlib import Path

import pygame
from pygame.transform import flip, scale_by
from pygame.sprite import Sprite, Group

STEAM_PIPE_SPRITESHEET_PATH = (
    Path(__file__).parent / "assets" / "steam_pipe" / "steam_pipe.png"
)


class SteamPipe(Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)

        frame_width, frame_height = 64, 32

        self.image = pygame.image.load(STEAM_PIPE_SPRITESHEET_PATH)
        self.frames = [
            scale_by(
                self.image.subsurface(
                    (0, i * frame_height, frame_width, frame_height)
                ),
                2.5,
            )
            for i in range(4)
        ]
        self.rect = pygame.FRect(self.frames[0].get_rect())

        self.animation_frame: int = 0
        self.animation_timer: float = 0
        self.animation_time: float = 1 / 12  # 12 fps
        self.flipped = False

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
        frame = flip(self.frames[self.animation_frame], self.flipped, False)
        surface.blit(frame, self.rect)  # type: ignore
