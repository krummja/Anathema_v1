from __future__ import annotations
from abc import ABC

import numpy as np
from anathema.abstracts import AbstractInitTiles


class InitTiles(AbstractInitTiles):

    _factory = None

    def initialize_tiles(self):
        if self._factory is not None:
            tiles = np.zeros((64, 64), dtype=object, order="F")
            for x in range(64):
                for y in range(64):
                    tiles[x, y] = self._factory.build(x, y)

            tiles[12, 12]['Renderable'].char = "≈"
            tiles[12, 12]['Renderable'].fore = 0xFF9999FF

            for x in range(9, 20):
                tiles[x, 8].destroy()
                tiles[x, 18].destroy()
                self._factory.build(x, 8, "▒", "0xFFAAAAFF", True, True)
                self._factory.build(x, 18, "▒", "0xFFAAAAFF", True, True)

            for y in range(9, 18):
                tiles[9, y].destroy()
                tiles[19, y].destroy()
                self._factory.build(9, y, "▒", "0xFFAAAAFF", True, True)
                self._factory.build(19, y, "▒", "0xFFAAAAFF", True, True)

            # NOTE An alternative way to do this -- build the map purely using NumPy,
            # i.e. with the usual amenities like slicing, and then at the end interpret
            # the array data and replace for real tile entities.
            return tiles
        else:
            raise Exception("No tile factory available to handle initialization.")

    @property
    def factory(self):
        return self._factory

    @factory.setter
    def factory(self, value) -> None:
        self._factory = value


class Tiles2D(AbstractInitTiles, ABC):
    """Abstract for a 2D array of Tiles."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        super().__init__()
