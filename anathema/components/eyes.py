from __future__ import annotations

from ecstremity import Component


class Eyes(Component):

    def __init__(self, vision: int = 8) -> None:
        self.vision = vision
