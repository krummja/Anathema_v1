from __future__ import annotations

from ecstremity import Component


class Equipment(Component):

    def __init__(self) -> None:
        self.slots = {
            'head': None,
            'chest': None,
            'legs': None,
            'hands': None,
            'feet': None
            }
