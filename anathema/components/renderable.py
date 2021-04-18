from __future__ import annotations
from typing import *
from ecstremity import Component


# class Renderable(Component):
#     def __init__(self, char: str, fore: str, back: Optional[str] = None) -> None:
#         self.char = char
#         self.fore = int(fore, base=16)
#         self.back = int(back, base=16) if back is not None else int("0x151515", base=16)

class Renderable(Component):

    def __init__(
            self,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            render_order: int = 0
        ) -> None:
        self.char = char
        self.color = color
        self.bg = bg
        self.render_order = render_order

    def __lt__(self, other: Renderable) -> bool:
        return self.render_order < other.render_order
