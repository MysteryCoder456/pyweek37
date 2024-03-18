from pathlib import Path
from random import randint

import pygame
from pygame import BLEND_ALPHA_SDL2, Vector2
from pygame.freetype import Font
from pygame.sprite import Group

from game.car import (
    CAR_ACCELERATION,
    CAR_STEER_SPEED,
    Car,
)
from game.road import Road

CAMERA_ACCELERATION = 2.5


def main():
    pygame.init()

    # Initialize display
    win_size = Vector2(1000, 750)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("The Boring Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    # Initialize fonts
    font_path = Path(__file__).parent / "assets" / "fonts" / "MPLUS1Code.ttf"
    font = Font(font_path)

    # Initialize game objects

    camera_speed: float = 15
    yt_views: float = 0

    car = Car()
    car.rect.centerx = win_size.x / 2  # type: ignore
    car.rect.centery = win_size.y * 0.8  # type: ignore
    car.angle = 90

    roads: Group[Road] = Group()  # type: ignore

    road1 = Road(win_size.y, roads)
    road1.rect.centerx = win_size.x / 2  # type: ignore
    road1.rect.bottom = win_size.y  # type: ignore

    road2 = Road(win_size.y, roads)
    road2.rect.centerx = win_size.x / 2  # type: ignore
    road2.rect.bottom = road1.rect.top  # type: ignore

    # Game events
    view_gain_event = pygame.USEREVENT + 1
    pygame.time.set_timer(view_gain_event, 15 * 1000)  # 15s interval

    while True:
        dt = clock.tick(fps) / 1000
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == view_gain_event:
                view_increase = randint(2, 5) * camera_speed * 0.02
                yt_views += view_increase

        # Car acceleration
        if keys[pygame.K_w]:
            car.speed += CAR_ACCELERATION
        elif keys[pygame.K_s]:
            car.speed -= CAR_ACCELERATION * 0.5

        # Car steering
        steer = int(keys[pygame.K_a]) - int(keys[pygame.K_d])
        car.angle += steer * car.speed / car.max_speed * CAR_STEER_SPEED

        # Camera motion
        # Camera never move faster than the car's maximum speed
        camera_speed = min(
            camera_speed + CAMERA_ACCELERATION * dt, car.max_speed * 0.9
        )

        # Update
        car.update(dt, camera_speed)
        roads.update(dt, camera_speed)

        # Move roads to give the illusion of infinite road
        if road1.rect.top > win_size.y:  # type: ignore
            road1.rect.bottom = road2.rect.top  # type: ignore
        if road2.rect.top > win_size.y:  # type: ignore
            road2.rect.bottom = road1.rect.top  # type: ignore

        # Decrease views if car goes offscreen or off road
        if not win.get_rect().contains(car.rect) or not (  # type: ignore
            road1.rect.left <= car.rect.centerx <= road1.rect.right  # type: ignore
        ):
            yt_views -= 8 * dt  # 8 views per second lost

        yt_views = max(0, yt_views)

        # NOTE: Draw Start
        win.fill((50, 50, 100))

        for road in roads:
            road.draw(win)

        car.draw(win)

        view_text, _ = font.render(f"{int(yt_views)} views", "white", size=24)
        win.blit(
            view_text,
            (5, 5),
            special_flags=BLEND_ALPHA_SDL2,
        )

        pygame.display.flip()
        # NOTE: Draw End
