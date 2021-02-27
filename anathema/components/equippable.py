from __future__ import annotations

from ecstremity import Component


class Equippable(Component):

    def __init__(self, body_part: str) -> None:
        self.body_part = body_part

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value) -> None:
        self._owner = value
