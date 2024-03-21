from pathlib import Path
from pygame import USEREVENT, Vector2

ASSETS_ROOT_DIR = Path(__file__).parent / "assets"
WINDOW_SIZE = Vector2(1000, 750)
GAME_STATE_CHANGE_EVENT = USEREVENT + 99
