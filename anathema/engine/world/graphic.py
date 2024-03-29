from __future__ import annotations
from typing import *
from dataclasses import dataclass

if TYPE_CHECKING:
    pass


@dataclass
class Graphic:
    char: int = ord("!")
    color: Tuple[int, int, int] = (255, 255, 255)
    bg: Tuple[int, int, int] = (0, 0, 0)
    render_order: int = 0

    def __lt__(self, other: Graphic) -> bool:
        return self.render_order < other.render_order
