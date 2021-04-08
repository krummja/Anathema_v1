from __future__ import annotations
from typing import *
from ecstremity import Component, Entity

from anathema.world.depth import Depth


class Position(Component):

    def __init__(self, x: int = 0, y: int = 0, z: Depth = Depth.GROUND) -> None:
        self.x: int = x
        self.y: int = y
        self.z: Depth = z

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def xyz(self) -> Tuple[int, int, Depth]:
        return self.x, self.y, self.z

    def __eq__(self, other: Union[Entity, Position]) -> bool:
        if isinstance(other, Entity):
            return (self.x == other['Position'].x and
                    self.y == other['Position'].y)
        elif isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __lt__(self, other: Union[Entity, Position]) -> bool:
        if isinstance(other, Entity):
            return (
                self != other['Position'] and
                self.z < other['Position'].z)
        elif isinstance(other, Position):
            return self != other and self.z < other.z
        else:
            return False
