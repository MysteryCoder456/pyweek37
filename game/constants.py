from pathlib import Path
from pygame import Vector2
from pygame.event import custom_type

ASSETS_ROOT_DIR = Path(__file__).parent / "assets"
DATA_ROOT_DIR = Path(__file__).parent / "data"
WINDOW_SIZE = Vector2(1000, 750)
GAME_STATE_CHANGE_EVENT = custom_type()
