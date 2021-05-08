from __future__ import annotations
from typing import *

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent
    from anathema.engine.world.tilemap import TileMap


class Position(Component):

    def __init__(self, area: TileMap, x: int, y: int) -> None:
        self.area = area
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y

    @property
    def ij(self):
        return self.y, self.x

    def distance_to(self, x: int, y: int) -> int:
        return max(abs(self.x - x), abs(self.y - y))

    def relative(self, x: int, y: int) -> Location:
        return Location(self.x + x, self.y + y)

    def adjacent(self) -> IndexExpression:
        return np.s_[self.y-1:self.y+1, self.x-1:self.x+1]
