import tcod
from tcod.tileset import Tileset


class Options:
    CONSOLE_WIDTH: int = 110
    CONSOLE_HEIGHT: int = 55
    TILESET: Tileset = tcod.tileset.load_tilesheet("font_16.png", 32, 8, tcod.tileset.CHARMAP_CP437)
    TITLE: str = "Anathema"
    VSYNC: bool = True
    STAGE_PANEL_WIDTH: int = 72
    STAGE_PANEL_HEIGHT: int = 39

    WORLD_WIDTH: int = 240
    WORLD_HEIGHT: int = 160
