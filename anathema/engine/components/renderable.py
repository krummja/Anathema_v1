from __future__ import annotations
from typing import *
from ecstremity import Component
from anathema.engine.world.tile import Tile


class Renderable(Component):

    def __init__(self, char: str, fg: Tuple[int, int, int]) -> None:
        self.char = ord(char)
        self.fg = fg
