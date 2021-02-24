from __future__ import annotations

from ecstremity import Component


class Openable(Component):

    def __init__(self, is_open: bool, open_char: str, closed_char: str) -> None:
        self._is_open = is_open
        self._open_char = open_char
        self._closed_char = closed_char

    @property
    def is_open(self) -> bool:
        return self._is_open
