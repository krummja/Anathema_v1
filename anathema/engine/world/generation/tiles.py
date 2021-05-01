from __future__ import annotations
from typing import *
from dataclasses import dataclass

from engine.world.generation.color import Color
from engine.world.tile import Tile

if TYPE_CHECKING:
    pass


@dataclass
class TileType:
    name: str
    char: str
    fore: Tuple[int, int, int]
    back: Tuple[int, int, int]

    _passable: Optional[bool] = None
    _opaque: Optional[bool] = None

    def open(self):
        self._passable = True
        self._opaque = False
        return self

    def solid(self):
        self._passable = False
        self._opaque = True
        return self

    def obstacle(self):
        self._passable = False
        self._opaque = False
        return self

    def obfuscated(self):
        self._passable = True
        self._opaque = True
        return self

    def passable(self):
        self._passable = True
        return self

    def opaque(self):
        self._opaque = True
        return self

    def make(self):
        move_cost = 1 if self._passable else 0
        transparent = not self._opaque
        back = self.back if self.back else (21, 21, 21)
        return Tile(self.name, move_cost, transparent, ord(self.char), self.fore, back)


def tile(
        name: str,
        char: str,
        fore: Tuple[int, int, int],
        back: Optional[Tuple[int, int, int]] = None
    ) -> TileType:
    return TileType(name, char, fore, back)


class Tiles:
    unformed = tile("unformed", "?", Color.light_cool_gray).open()
    unformed_wet = tile("unformed_wet", "≈", Color.light_blue).open()
    open_ground = tile("open", ".", Color.white).open()
    solid = tile("solid", "#", Color.light_cool_gray).solid()
    passage = tile("passage", "-", Color.light_cool_gray).open()
    solid_wet = tile("solid_wet", "≈", Color.cool_gray).obstacle()
    passage_wet = tile("passage_wet", "≈", Color.light_blue).open()
    doorway = tile("doorway", "○", Color.light_cool_gray).open()

    flagstone_wall = tile("Flagstone Wall", "▒", Color.light_warm_gray, Color.warm_gray).solid()
    granite_wall = tile("Granite Wall", "▒", Color.cool_gray).solid()
    granite_1 = tile("Granite", "▓", Color.dark_cool_gray).solid()

    flagstone_floor = tile("Flagstone Floor", ".", Color.warm_gray, Color.dark_warm_gray).open()
    granite_floor = tile("Granite Floor", ".", Color.dark_cool_gray, Color.darker_cool_gray).open()

    dirt_1 = tile("Dirt", "·", Color.brown).open()
    dirt_2 = tile("Dirt", "φ", Color.brown).open()
    grass = tile("Grass", "░", Color.lima).open()
    tall_grass = tile("Tall Grass", "√", Color.pea_green).obfuscated()
    tree_1 = tile("Evergreen Tree", "▲", Color.sherwood).solid()
    shallow_water = tile("Shallow Water", "≈", Color.light_blue).open()
