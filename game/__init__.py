from pathlib import Path
from random import randint, random

import pygame
from pygame import BLEND_ALPHA_SDL2, Vector2
from pygame.freetype import STYLE_STRONG, Font
from pygame.sprite import Group, collide_mask, spritecollide
from pygame.transform import scale_by

CAMERA_ACCELERATION = 2.0
ASSETS_ROOT_DIR = Path(__file__).parent / "assets"

# There are imported here to avoid cyclic imports
from game.car import (  # noqa: E402
    CAR_ACCELERATION,
    CAR_STEER_SPEED,
    Car,
)
from game.road import Road  # noqa: E402
from game.steam_pipe import SteamPipe  # noqa: E402


def main():
    pygame.init()

    # Initialize display
    win_size = Vector2(1000, 750)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("The Boring Game")

    # Initialize clock
    fps = 60
    clock = pygame.time.Clock()

    # Initialize assets

    font_path = ASSETS_ROOT_DIR / "fonts" / "MPLUS1Code.ttf"
    font = Font(font_path)

    heart_sprite_path = ASSETS_ROOT_DIR / "heart" / "heart.png"
    heart_sprite = scale_by(pygame.image.load(heart_sprite_path), 2.5)

    # Game variables

    camera_speed: float = 30
    yt_views: float = 0
    health: int = 3
    game_over = False

    # Initialize game objects

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

    pipes: Group[SteamPipe] = Group()  # type: ignore

    # Game events

    view_gain_event = pygame.USEREVENT + 1
    pygame.time.set_timer(view_gain_event, 10 * 1000)  # 10s interval

    pipe_spawn_event = pygame.USEREVENT + 2
    pygame.time.set_timer(pipe_spawn_event, 3 * 1000)  # 3s interval

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

            elif event.type == pipe_spawn_event:
                if random() <= 0.3:  # 70% chance to spawn
                    continue

                pipe = SteamPipe(pipes)
                pipe.rect.bottom = 0  # type: ignore

                # Equally likely to spawn on either side
                if random() < 0.5:
                    pipe.rect.left = road1.rect.left  # type: ignore
                else:
                    pipe.rect.right = road1.rect.right  # type: ignore
                    pipe.flipped = True

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
        camera_speed = (
            min(camera_speed + CAMERA_ACCELERATION * dt, car.max_speed * 0.9)
            if not game_over
            else 0
        )

        # Update
        car.update(dt, camera_speed)
        roads.update(dt, camera_speed)
        pipes.update(dt, camera_speed)

        # Destroy offscreen pipes
        pipes.remove([pipe for pipe in pipes if pipe.rect.top > win_size.y])  # type: ignore

        # Car - pipe collision
        for pipe in spritecollide(car, pipes, dokill=True, collided=collide_mask):  # type: ignore
            health -= 1

            if health <= 0:
                game_over = True

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

        if not game_over:
            car.draw(win)

        for pipe in pipes:
            pipe.draw(win)

        # Draw view count
        view_text, _ = font.render(f"{int(yt_views)} views", "white", size=28)
        win.blit(
            view_text,
            (5, 5),
            special_flags=BLEND_ALPHA_SDL2,
        )

        # Draw hearts
        for i in range(health):
            win.blit(
                heart_sprite,
                (
                    win_size.x - 5 - (1.15 * i + 1) * heart_sprite.get_width(),
                    5,
                ),
            )

        # Draw game over text
        if game_over:
            game_over_text, game_over_rect = font.render(
                "GAME OVER", "RED", size=64, style=STYLE_STRONG
            )
            win.blit(
                game_over_text,
                (
                    (win_size.x - game_over_rect.width) / 2,
                    (win_size.y - game_over_rect.height) / 2,
                ),
                special_flags=BLEND_ALPHA_SDL2,
            )

        pygame.display.flip()
        # NOTE: Draw End
