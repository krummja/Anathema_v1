from __future__ import annotations
from typing import Optional
import numpy as np

from dataclasses import dataclass


@dataclass
class Color:

    r: int
    g: int
    b: int
    a: int = 0x00

    def make(self) -> str:
        a = self.a << 24
        r = self.r << 16
        g = self.g << 8
        b = self.b << 0
        return hex(a + r + g + b)


class Palette:
    black = Color(0x00, 0x00, 0x00).make()
    white = Color(0xFF, 0xFF, 0xFF).make()

    light_cool_gray = Color(0x74, 0x92, 0xb5).make()
    cool_gray = Color(0x3f, 0x4b, 0x73).make()
    dark_cool_gray = Color(0x26, 0x2a, 0x42).make()
    darker_cool_gray = Color(0x14, 0x13, 0x1f).make()

    light_warm_gray = Color(0x84, 0x7e, 0x87).make()
    warm_gray = Color(0x48, 0x40, 0x4a).make()
    dark_warm_gray = Color(0x2a, 0x24, 0x2b).make()
    darker_warm_gray = Color(0x16, 0x11, 0x17).make()

    sandal = Color(0xbd, 0x90, 0x6c).make()
    tan = Color(0x8e, 0x52, 0x37).make()
    brown = Color(0x99, 0x6a, 0x56).make()
    dark_brown = Color(0x5c, 0x47, 0x3e).make()

    light_blue = Color(0x40, 0xa3, 0xe5).make()
    blue = Color(0x15, 0x57, 0xc2).make()
    dark_blue = Color(0x1a, 0x2e, 0x96).make()

    mint = Color(0x81, 0xd9, 0x75).make()
    lima = Color(0x83, 0x9e, 0x0d).make()
    pea_green = Color(0x16, 0x75, 0x26).make()
    sherwood = Color(0x00, 0x40, 0x27).make()

