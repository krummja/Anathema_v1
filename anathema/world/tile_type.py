from __future__ import annotations
from typing import Optional
from dataclasses import dataclass


@dataclass
class TileType:

    name: str
    char: str
    fore: int

    _blocker: Optional[bool] = None
    _opaque: Optional[bool] = None
    _on_open = None
    _on_close = None

    def open(self):
        self._blocker = False
        self._opaque = False
        return self

    def solid(self):
        self._blocker = True
        self._opaque = True
        return self

    def impassable(self):
        self._blocker = True
        self._opaque = False
        return self

    def obfuscated(self):
        self._blocker = False
        self._opaque = True
        return self

    def on_open(self, func):
        self._on_open = func
        return self

    def on_close(self, func):
        self._on_close = func
        return self

    def door(self):
        return self
