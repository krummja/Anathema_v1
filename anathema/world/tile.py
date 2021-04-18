from __future__ import annotations
from typing import *
import numpy as np


tile_graphic = np.dtype([
    ("ch", np.int),
    ("fg", "3B"),
    ("bg", "3B")
])


tile_dt = np.dtype([
    ("move_cost", np.uint8),
    ("transparent", np.bool),
    ("light", tile_graphic),
    ("dark", tile_graphic)
])


class Graphic:
    def __init__(
            self,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            render_order: int = 0
        ) -> None:
        self.char = char
        self.color = color
        self.bg = bg
        self.render_order = render_order

    def __lt__(self, other: Graphic) -> bool:
        return self.render_order < other.render_order


class Tile(Graphic):

    def __new__(
            cls,
            uid: str,
            move_cost: int,
            transparent: bool,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int]
        ) -> np.ndarray:
        instance = super(Tile, cls).__new__(cls)
        instance.__init__(uid, move_cost, transparent, char, color, bg)

        light = (char, color, bg)
        dark = (char,
                (color[0] // 2, color[1] // 2, color[2] // 2),
                (bg[0] // 2, bg[1] // 2, bg[2] // 2))

        return np.array((move_cost, transparent, light, dark), dtype=tile_dt)

    def __init__(
            self,
            uid: str,
            move_cost: int,
            transparent: bool,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int]
    ) -> None:
        super().__init__(char, color, bg)
        self.uid = uid
        self.move_cost = move_cost
        self.transparent = transparent
        self.char = char
        self.color = color
        self.bg = bg
