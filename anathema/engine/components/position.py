from __future__ import annotations
from typing import *

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Position(Component):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y

    @property
    def ij(self):
        return self.y, self.x
