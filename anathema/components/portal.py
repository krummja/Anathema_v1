from __future__ import annotations

from ecstremity import Component


class Portal(Component):

    def __init__(self, area_from: str, area_to: str) -> None:
        self.area_from = area_from
        self.area_to = area_to
