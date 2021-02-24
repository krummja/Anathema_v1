from __future__ import annotations

from ecstremity import Component


class Eyes(Component):

    def __init__(self, vision: int = 8, eye_count: int = 2) -> None:
        self.vision = vision
        self._eye_count = eye_count
