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

    @staticmethod
    def black():
        return Color(0x00, 0x00, 0x00).make()

    @staticmethod
    def white():
        return Color(0xFF, 0xFF, 0xFF).make()

    @staticmethod
    def brown():
        return Color(0x99, 0x6a, 0x56).make()

    @staticmethod
    def dark_brown():
        return Color(0x5c, 0x47, 0x3e).make()

    @staticmethod
    def light_blue():
        return Color(0x40, 0xa3, 0xe5).make()

    @staticmethod
    def light_cool_gray():
        return Color(0x74, 0x92, 0xb5).make()

    @staticmethod
    def cool_gray():
        return Color(0x3f, 0x4b, 0x73).make()

    @staticmethod
    def light_warm_gray():
        return Color(0x84, 0x7e, 0x87).make()

    @staticmethod
    def dark_cool_gray():
        return Color(0x26, 0x2a, 0x42).make()

    @staticmethod
    def warm_gray():
        return Color(0x48, 0x40, 0x4a).make()

    @staticmethod
    def mint():
        return Color(0x81, 0xd9, 0x75).make()

    @staticmethod
    def lima():
        return Color(0x83, 0x9e, 0x0d).make()

    @staticmethod
    def pea_green():
        return Color(0x16, 0x75, 0x26).make()

    @staticmethod
    def sherwood():
        return Color(0x00, 0x40, 0x27).make()

    def make(self) -> str:
        a = self.a << 24
        r = self.r << 16
        g = self.g << 8
        b = self.b << 0
        return hex(a + r + g + b)