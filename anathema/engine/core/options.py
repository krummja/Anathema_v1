import tcod
from tcod.tileset import Tileset


class Options:
    CONSOLE_WIDTH: int = 110
    CONSOLE_HEIGHT: int = 55
    TILESET: Tileset = tcod.tileset.load_tilesheet("font_16.png", 32, 8, tcod.tileset.CHARMAP_CP437)
    TITLE: str = "Anathema"
    VSYNC: bool = True
