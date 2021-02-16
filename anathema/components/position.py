from __future__ import annotations
from typing import Tuple

from ecstremity import Component


class Position(Component):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y
