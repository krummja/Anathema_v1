import tcod
from tcod.tileset import Tileset
from anathema.data import get_data


class Options:
    CONSOLE_WIDTH: int = 110
    CONSOLE_HEIGHT: int = 65
    TILESET: Tileset = tcod.tileset.load_tilesheet(get_data("font_16.png"), 32, 8, tcod.tileset.CHARMAP_CP437)
    TITLE: str = "Anathema"
    VSYNC: bool = True
    STAGE_PANEL_WIDTH: int = 72
    STAGE_PANEL_HEIGHT: int = 50

    AREA_SIZE: int = 512
    WORLD_WIDTH: int = 240
    WORLD_HEIGHT: int = 160
