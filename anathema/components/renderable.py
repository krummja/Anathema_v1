from __future__ import annotations

from ecstremity import Component


class Renderable(Component):
    def __init__(self, char: str, fore: str) -> None:
        self.char = char
        self.fore = int(fore, base=16)
