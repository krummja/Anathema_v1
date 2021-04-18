from __future__ import annotations
from typing import *
import numpy as np
from dataclasses import dataclass

from .tile import tile_dt
from .region import Region

if TYPE_CHECKING:
    from numpy.lib.index_tricks import IndexExpression


class Location:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y

    @xy.setter
    def xy(self, value: Tuple[int, int]) -> None:
        self.x, self.y = value

    @property
    def ij(self) -> Tuple[int, int]:
        return self.y, self.x

    def distance_to(self, x: int, y: int) -> int:
        return max(abs(self.x - x), abs(self.y - y))

    def relative(self, x: int, y: int) -> Location:
        return Location(self.x + x, self.y + y)

    def adjacent(self) -> IndexExpression:
        return np.s_[self.y-1:self.y+1, self.x-1:self.x+1]


class AreaLocation(Location):

    def __init__(self, area: Area, x: int, y: int) -> None:
        self.area = area
        super().__init__(x, y)


class Area:

    def __init__(self, name: str, region: Region, width: int, height: int) -> None:
        self.name = name
        self.region = region
        self.width = width
        self.height = height
        self._tiles = np.zeros(self.shape, dtype=tile_dt)
        self._explored = np.zeros(self.shape, dtype=bool)
        self._visible = np.zeros(self.shape, dtype=bool)

    @property
    def shape(self) -> Tuple[int, int]:
        return self.height, self.width

    @property
    def tiles(self):
        return self._tiles

    @property
    def explored(self):
        return self._explored

    @property
    def visible(self):
        return self._visible

    def get_bg_color(self, x: int, y: int) -> List[int]:
        pass

    def __getitem__(self, key: Tuple[int, int]) -> AreaLocation:
        return AreaLocation(self, *key)
