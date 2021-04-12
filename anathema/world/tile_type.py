from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class TileType:
    name: str
    char: str
    fore: int
    back: int

    blocker: Optional[bool] = None
    opaque: Optional[bool] = None
    interactable: Optional[bool] = None
    portal: Optional[bool] = None
    is_closed: Optional[bool] = None
    is_container: Optional[bool] = None

    def open(self) -> TileType:
        self.blocker = False
        self.opaque = False
        return self

    def solid(self) -> TileType:
        self.blocker = True
        self.opaque = True
        return self

    def obstacle(self) -> TileType:
        self.blocker = True
        self.opaque = False
        return self

    def obfuscated(self) -> TileType:
        self.blocker = False
        self.opaque = True
        return self

    def openable(self) -> TileType:
        self.interactable = True
        self.is_closed = True
        return self

    def closable(self) -> TileType:
        self.interactable = True
        self.is_closed = False
        return self

    def door(self) -> TileType:
        self.portal = True
        self.blocker = True
        self.opaque = True
        return self

    def container(self) -> TileType:
        self.is_container = True
        return self
