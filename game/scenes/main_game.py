import os
from random import randint, random

import pygame
from pygame import BLEND_ALPHA_SDL2, KEYDOWN, KEYUP
from pygame.freetype import STYLE_STRONG, Font
from pygame.sprite import Group, collide_mask
from pygame.transform import scale_by
from pygame.event import custom_type
from pygame.mixer import Sound, Channel

from game.game_state import GameState
from game.constants import (
    ASSETS_ROOT_DIR,
    DATA_ROOT_DIR,
    WINDOW_SIZE,
    GAME_STATE_CHANGE_EVENT,
    CAMERA_ACCELERATION,
)
from game.scene import Scene
from game.car import (
    CAR_ACCELERATION,
    CAR_STEER_SPEED,
    Car,
)
from game.road import Road
from game.steam_pipe import SteamPipe
from game.test_tube import TestTube


class MainGameScene(Scene):
    def on_enter(self) -> None:
        # Initialize assets

        font_path = ASSETS_ROOT_DIR / "fonts" / "MPLUS1Code.ttf"
        self.font = Font(font_path)

        heart_sprite_path = ASSETS_ROOT_DIR / "heart" / "heart.png"
        self.heart_sprite = scale_by(pygame.image.load(heart_sprite_path), 2.5)

        accelerate_sfx_path = ASSETS_ROOT_DIR / "car" / "accelerate.wav"
        self.accelerate_sfx = Sound(accelerate_sfx_path)

        death_sfx_path = ASSETS_ROOT_DIR / "car" / "death.wav"
        self.death_sfx = Sound(death_sfx_path)

        self.car_sfx_channel = Channel(0)
        self.car_sfx_channel.set_volume(0.6)

        pipe_sfx_path = ASSETS_ROOT_DIR / "steam_pipe" / "hit.wav"
        self.pipe_hit_sfx = Sound(pipe_sfx_path)

        tube_sfx_path = ASSETS_ROOT_DIR / "test_tube" / "hit.wav"
        self.tube_hit_sfx = Sound(tube_sfx_path)

        self.obstacle_sfx_channel = Channel(1)
        self.obstacle_sfx_channel.set_volume(0.7)

        # Load high score

        self.high_score_path = DATA_ROOT_DIR / "high_score.txt"

        if os.path.exists(self.high_score_path):
            with open(self.high_score_path) as f:
                self.high_score = int(f.read())
        else:
            self.high_score = None

        # Game variables

        self.camera_speed: float = 35
        self.yt_views: float = 0
        self.health: int = 3
        self.game_over = False

        # Initialize game objects

        self.car = Car()
        self.car.rect.centerx = WINDOW_SIZE.x / 2  # type: ignore
        self.car.rect.centery = WINDOW_SIZE.y * 0.75  # type: ignore
        self.car.angle = 90

        self.roads: Group[Road] = Group()  # type: ignore

        self.road1 = Road(WINDOW_SIZE.y, self.roads)
        self.road1.rect.centerx = WINDOW_SIZE.x / 2  # type: ignore
        self.road1.rect.bottom = WINDOW_SIZE.y  # type: ignore

        self.road2 = Road(WINDOW_SIZE.y, self.roads)
        self.road2.rect.centerx = WINDOW_SIZE.x / 2  # type: ignore
        self.road2.rect.bottom = self.road1.rect.top  # type: ignore

        self.pipes: Group[SteamPipe] = Group()  # type: ignore
        self.tubes: Group[TestTube] = Group()  # type: ignore

        # Game events

        self.view_gain_event = custom_type()
        pygame.time.set_timer(self.view_gain_event, 10 * 1000)  # 10s interval

        self.pipe_spawn_event = custom_type()
        pygame.time.set_timer(self.pipe_spawn_event, 3 * 1000)  # 3s interval

        self.tube_spawn_event = custom_type()

        self.begin_tube_spawning_event = custom_type()
        pygame.time.set_timer(
            self.begin_tube_spawning_event, 60 * 1000
        )  # Begin spawning tubes after 60s

        self.game_over_event = custom_type()

    def on_event(self, event: pygame.Event) -> None:
        if event.type == self.view_gain_event and not self.game_over:
            view_increase = randint(2, 5) * self.camera_speed * 0.02
            self.yt_views += view_increase

        elif event.type == self.pipe_spawn_event:
            if random() <= 0.35:  # 65% chance to spawn
                return

            pipe = SteamPipe(self.pipes)
            pipe.rect.bottom = 0  # type: ignore

            # Equally likely to spawn on either side
            if random() < 0.5:
                pipe.rect.left = self.road1.rect.left  # type: ignore
            else:
                pipe.rect.right = self.road1.rect.right  # type: ignore
                pipe.flipped = True

        elif event.type == self.tube_spawn_event:
            if random() <= 0.50:  # 50% chance to spawn
                return

            tube = TestTube(self.tubes)
            tube.rect.bottom = 0  # type: ignore

            # Equally likely to spawn on either side
            road_quarter_width = self.road1.rect.width / 4  # type: ignore
            if random() < 0.5:
                tube.rect.centerx = self.road1.rect.left + road_quarter_width  # type: ignore
            else:
                tube.rect.centerx = self.road1.rect.right - road_quarter_width  # type: ignore

        elif event.type == self.begin_tube_spawning_event:
            pygame.time.set_timer(
                self.tube_spawn_event, 20 * 1000
            )  # 20s interval

            # Cancel begin tube spawning event
            pygame.time.set_timer(self.begin_tube_spawning_event, 0)

        elif event.type == self.game_over_event:
            # Update high score
            self.high_score = max(int(self.yt_views), self.high_score or 0)
            with open(self.high_score_path, "w") as f:
                f.write(str(self.high_score))

            # Transition scene to main menu afer 5s
            event = pygame.Event(
                GAME_STATE_CHANGE_EVENT,
                {"new_state": GameState.MAIN_MENU},
            )
            pygame.time.set_timer(event, 5000)

            # Play SFX
            self.car_sfx_channel.play(self.death_sfx)

        elif event.type == KEYDOWN:
            if event.key == pygame.K_w:
                self.car_sfx_channel.play(self.accelerate_sfx, loops=-1)

        elif event.type == KEYUP:
            if (
                event.key == pygame.K_w
                and self.car_sfx_channel.get_sound() == self.accelerate_sfx
            ):
                self.car_sfx_channel.stop()

    def on_update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        # Car acceleration
        if keys[pygame.K_w]:
            self.car.speed += CAR_ACCELERATION
        elif keys[pygame.K_s]:
            self.car.speed -= CAR_ACCELERATION * 0.5

        # Car steering
        steer = int(keys[pygame.K_a]) - int(keys[pygame.K_d])
        self.car.angle += (
            steer * self.car.speed / self.car.max_speed * CAR_STEER_SPEED
        )

        # Camera motion
        # Camera never move faster than the car's maximum speed
        self.camera_speed = (
            min(
                self.camera_speed + CAMERA_ACCELERATION * dt,
                self.car.max_speed * 0.8,
            )
            if not self.game_over
            else 0
        )

        # Update
        self.car.update(dt, self.camera_speed)
        self.roads.update(dt, self.camera_speed)
        self.pipes.update(dt, self.camera_speed)
        self.tubes.update(dt, self.camera_speed)

        for pipe in self.pipes:
            # Destroy offscreen pipes
            if pipe.rect.top > WINDOW_SIZE.y:  # type: ignore
                self.pipes.remove(pipe)

            # Car - pipe collision
            if collide_mask(self.car, pipe):
                self.health -= 1
                self.pipes.remove(pipe)
                self.obstacle_sfx_channel.play(self.pipe_hit_sfx)

                # Check for game over
                if self.health <= 0:
                    self.game_over = True
                    pygame.event.post(pygame.Event(self.game_over_event))
                    break

        for tube in self.tubes:
            # Destroy offscreen tubes
            if tube.rect.top > WINDOW_SIZE.y:  # type: ignore
                self.tubes.remove(tube)

            # Car - pipe collision
            if collide_mask(self.car, tube):
                self.health -= 1
                self.tubes.remove(tube)
                self.obstacle_sfx_channel.play(self.tube_hit_sfx)

                # Check for game over
                if self.health <= 0:
                    self.game_over = True
                    pygame.event.post(pygame.Event(self.game_over_event))
                    break

                view_increase = randint(10, 15) * self.camera_speed * 0.02
                self.yt_views += view_increase

        # Move roads to give the illusion of infinite road
        if self.road1.rect.top > WINDOW_SIZE.y:  # type: ignore
            self.road1.rect.bottom = self.road2.rect.top  # type: ignore
        if self.road2.rect.top > WINDOW_SIZE.y:  # type: ignore
            self.road2.rect.bottom = self.road1.rect.top  # type: ignore

        # Decrease views if car goes offscreen or off road
        win_rect = pygame.FRect(0, 0, WINDOW_SIZE.x, WINDOW_SIZE.y)
        if not self.game_over and not (
            win_rect.contains(self.car.rect)  # type: ignore
            and (
                self.road1.rect.left <= self.car.rect.centerx <= self.road1.rect.right  # type: ignore
            )
        ):
            self.yt_views -= 8 * dt  # 8 views per second lost
            self.yt_views = max(0, self.yt_views)

    def on_draw(self, window: pygame.Surface) -> None:
        window.fill((50, 50, 100))

        for road in self.roads:
            road.draw(window)

        for tube in self.tubes:
            tube.draw(window)

        if not self.game_over:
            self.car.draw(window)

        for pipe in self.pipes:
            pipe.draw(window)

        # Draw view count
        view_text, view_rect = self.font.render(
            f"{int(self.yt_views)} views", "white", size=24
        )
        window.blit(
            view_text,
            (5, 5),
            special_flags=BLEND_ALPHA_SDL2,
        )

        # Draw best view count
        if high_score := self.high_score:
            high_score_text, _ = self.font.render(
                f"Best: {high_score} views", "white", size=24
            )
            window.blit(
                high_score_text,
                (5, view_rect.bottom + 5),
                special_flags=BLEND_ALPHA_SDL2,
            )

        # Draw hearts
        for i in range(self.health):
            window.blit(
                self.heart_sprite,
                (
                    WINDOW_SIZE.x
                    - 5
                    - (1.15 * i + 1) * self.heart_sprite.get_width(),
                    5,
                ),
            )

        # Draw game over text
        if self.game_over:
            game_over_text, game_over_rect = self.font.render(
                "LIVESTREAM ENDED", "RED", size=64, style=STYLE_STRONG
            )
            window.blit(
                game_over_text,
                (
                    (WINDOW_SIZE.x - game_over_rect.width) / 2,
                    (WINDOW_SIZE.y - game_over_rect.height) / 2,
                ),
                special_flags=BLEND_ALPHA_SDL2,
            )

        pygame.display.flip()
