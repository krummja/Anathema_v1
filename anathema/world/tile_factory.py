from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

from anathema.utils.geometry import Rect, Point, Size


if TYPE_CHECKING:
    from anathema.world.area import Area
    from ecstremity import Engine, Entity


class Depth(Enum):
    ABOVE_5 = 10
    ABOVE_4 = 9
    ABOVE_3 = 8
    ABOVE_2 = 7
    ABOVE_1 = 6
    GROUND  = 5
    BELOW_1 = 4
    BELOW_2 = 3
    BELOW_3 = 2
    BELOW_4 = 1


@dataclass
class TileType:

    name: str
    char: str
    fore: int

    _blocker: Optional[bool] = None
    _opaque: Optional[bool] = None
    _on_open = None
    _on_close = None

    def open(self):
        self._blocker = False
        self._opaque = False
        return self

    def solid(self):
        self._blocker = True
        self._opaque = True
        return self

    def on_open(self, func):
        self._on_open = func
        return self

    def on_close(self, func):
        self._on_close = func
        return self

    def door(self):
        return self


light_cool_gray = "0x7492b5"
cool_gray = "0x3f4b73"
light_blue = "0x40a3e5"


class Tiles:

    @staticmethod
    def unformed():
        return Tiles.tile("unformed", "?", light_cool_gray).open()

    @staticmethod
    def unformed_wet():
        return Tiles.tile("unformed_wet", "≈", cool_gray).open()

    @staticmethod
    def open():
        return Tiles.tile("open", "·", light_cool_gray).open()

    @staticmethod
    def solid():
        return Tiles.tile("solid", "#", light_cool_gray).solid()

    @staticmethod
    def passage():
        return Tiles.tile("passage", "-", light_cool_gray).open()

    @staticmethod
    def solid_wet():
        return Tiles.tile("solid_wet", "≈", light_blue).solid()

    @staticmethod
    def tile(name: str, char: str, fore: int):
        return TileType(name, char, fore)


class TileSpace:

    @staticmethod
    def initialize():
        tile_space = np.zeros((64, 64), dtype=object, order="F")

        #! Point where specific generators may intervene.

        tile_space[:, :] = Tiles.open()

        room = Rect(Point(5, 5), Size(10, 10))
        tile_space[room.outer] = Tiles.solid()
        tile_space[room.inner] = Tiles.open()
        tile_space[room.top_left.x+3:room.top_left.x+6] = Tiles.open()

        return tile_space


class TileFactory:

    def __init__(self, area: Area, ecs: Engine) -> None:
        self.area = area
        self.ecs = ecs
        self.tile_space = TileSpace.initialize()

    def build(self):
        for x in range(self.area.width):
            for y in range(self.area.height):
                tile_def = self.tile_space[x, y]
                tile = self.ecs.create_entity()

                tile.add('Position', {'x': x, 'y': y, 'z': Depth.GROUND})
                tile.add('Renderable', {'char': tile_def.char, 'fore': tile_def.fore})

                if tile_def._blocker:
                    tile.add('Blocker', {})
                if tile_def._opaque:
                    tile.add('Opaque', {})
