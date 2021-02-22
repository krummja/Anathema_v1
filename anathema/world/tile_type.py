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
    _interactable: Optional[bool] = None
    _portal: Optional[bool] = None
    _is_closed: Optional[bool] = None

    def open(self) -> TileType:
        self._blocker = False
        self._opaque = False
        return self

    def solid(self) -> TileType:
        self._blocker = True
        self._opaque = True
        return self

    def impassable(self) -> TileType:
        self._blocker = True
        self._opaque = False
        return self

    def obfuscated(self) -> TileType:
        self._blocker = False
        self._opaque = True
        return self

    def openable(self) -> TileType:
        self._is_closed = True
        return self

    def closable(self) -> TileType:
        self._is_closed = False
        return self

    def door(self) -> TileType:
        self._interactable = True
        self._portal = True
        self._blocker = True
        self._opaque = True
        return self
