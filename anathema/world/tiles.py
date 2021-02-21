from __future__ import annotations

from anathema.world.tile_factory import TileFactory, Depth


class Tiles:

    def tile(self, name: str, char: str, fore: int) -> TileBuilder:
        return TileBuilder(name, char, fore)


class TileBuilder:

    def __init__(self, name: str, char: str, fore: int) -> None:
        self.name = name
        self.char = char
        self.fore = fore

    def solid(self):
        pass

    def water(self):
        pass

    def _motility(self):
        return TileType()


class TileType:

    def __init__(self, name: str, glyphs, motility, portal, on_close, on_open) -> None:
        self.name = name
        self.glyphs = glyphs
        self.motility = motility
        self.portal = portal
        self.on_close = on_close
        self.on_open = on_open

    @property
    def can_open(self) -> bool:
        return True if self.on_open else False

    @property
    def can_close(self) -> bool:
        return True if self.on_close else False


class Motility:
    pass


class TilePortal:
    pass


class Tile:
    def __init__(self) -> None:
        self.tile_type: TileType
