from __future__ import annotations

from ecstremity import Component


class Equippable(Component):

    def __init__(self, slot_type) -> None:
        self.slot_type = slot_type
