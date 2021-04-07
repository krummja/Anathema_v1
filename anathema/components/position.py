from __future__ import annotations
from typing import *
from ecstremity import Component


class Position(Component):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x
        self.y: int = y

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def ij(self) -> Tuple[int, int]:
        return self.y, self.x
