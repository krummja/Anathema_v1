from __future__ import annotations
from typing import *
from ecstremity import Component


class Renderable(Component):
    def __init__(self, char: str, fore: str, back: Optional[str] = None) -> None:
        self.char = char
        self.fore = int(fore, base=16)
        self.back = int(back, base=16) if back is not None else int("0x151515", base=16)
