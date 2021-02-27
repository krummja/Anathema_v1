from __future__ import annotations
from typing import Optional, Tuple

from ecstremity import Component


class Position(Component):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.h_clamp = None
        self.v_clamp = None


    @property
    def horizontal(self) -> Tuple[int, int]:
        return self.h_clamp

    @horizontal.setter
    def horizontal(self, left: int, right: int) -> None:
        self.h_clamp = (left, right)

    @property
    def vertical(self) -> Tuple[int, int]:
        return self.v_clamp

    @vertical.setter
    def vertical(self, top: int, bottom: int) -> None:
        self.v_clamp = (top, bottom)
