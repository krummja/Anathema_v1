from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Color:

    r: int
    g: int
    b: int

    @staticmethod
    def black(): return Color(0x00, 0x00, 0x00)
