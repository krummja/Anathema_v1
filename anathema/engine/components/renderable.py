from __future__ import annotations
from typing import *
from ecstremity import Component
from anathema.engine.world.tile import Tile


class Renderable(Component):

    def __init__(self, char: Union[str, int], fg: Tuple[int, int, int]) -> None:
        if isinstance(char, str):
            self.char = ord(char)
        else:
            self.char = char
        self.fg = fg
