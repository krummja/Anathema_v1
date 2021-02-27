from __future__ import annotations

from ecstremity import Component


class Title(Component):

    def __init__(self, text: str) -> None:
        self.text = text
