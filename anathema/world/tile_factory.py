from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

from anathema.utils.color import Color
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


class Tiles:

    @staticmethod
    def unformed():
        return Tiles.tile("unformed", "?", Color.light_cool_gray()).open()

    @staticmethod
    def unformed_wet():
        return Tiles.tile("unformed_wet", "≈", Color.cool_gray()).open()

    @staticmethod
    def open():
        return Tiles.tile("open", "·", Color.light_cool_gray()).open()

    @staticmethod
    def solid():
        return Tiles.tile("solid", "#", Color.light_cool_gray()).solid()

    @staticmethod
    def passage():
        return Tiles.tile("passage", "-", Color.light_cool_gray()).open()

    @staticmethod
    def solid_wet():
        return Tiles.tile("solid_wet", "≈", Color.light_blue()).solid()

    @staticmethod
    def passage_wet():
        return Tiles.tile("passage_wet", "-", Color.light_blue()).open()

    @staticmethod
    def doorway():
        return Tiles.tile("doorway", "○", Color.light_cool_gray()).open()

    @staticmethod
    def flagstone_wall():
        return Tiles.tile("flagstone_wall", "▒", Color.light_warm_gray()).solid()

    @staticmethod
    def flagstone_floor():
        return Tiles.tile("flagstone_floor", "·", Color.warm_gray()).open()

    @staticmethod
    def tile(name: str, char: str, fore: Color):

        return TileType(name, char, fore)


class TileSpace:

    @staticmethod
    def initialize():
        tile_space = np.zeros((64, 64), dtype=object, order="F")

        #! Point where specific generators may intervene.

        tile_space[:, :] = Tiles.flagstone_floor()

        room = Rect(Point(5, 5), Size(10, 10))
        tile_space[room.outer] = Tiles.flagstone_wall()
        tile_space[room.inner] = Tiles.flagstone_floor()
        tile_space[room.top_left.x+3:room.top_left.x+6, room.top] = Tiles.flagstone_floor()

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
