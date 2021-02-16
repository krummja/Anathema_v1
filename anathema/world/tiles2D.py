from __future__ import annotations
from abc import ABC, abstractmethod

from anathema.abstracts import AbstractInitTiles


class InitTiles(AbstractInitTiles):

    _factory = None

    def initialize_tiles(self):
        if self._factory is not None:
            tiles = [[ self._factory.build(x, y) for x in range(self.width)  ]
                                                 for y in range(self.height) ]
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

    def get_entity_at_pos(self, x: int, y: int):
        tile = self.tiles[x][y]
        # TODO Figure out a good way to query the map to get uids at pos
