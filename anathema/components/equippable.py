from __future__ import annotations

from ecstremity import Component


class Equippable(Component):

    def __init__(self, body_part: str, is_container: int = 0) -> None:
        self.body_part = body_part
        self._is_container = is_container

    @property
    def is_container(self) -> bool:
        return bool(self._is_container)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value) -> None:
        self._owner = value
