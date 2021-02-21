from __future__ import annotations

from ecstremity import Component


class Mana(Component):

    def __init__(self, base: int) -> None:
        self._BASE_MANA = base
        self._EXPENDED: int = 0

    @property
    def current(self) -> int:
        return self._BASE_MANA - self._EXPENDED

    def expend(self, value: int) -> None:
        self._EXPENDED += value

    def apply(self, value: int) -> None:
        self.expend(value * -1)

    def __str__(self) -> str:
        return f"{self.current} / {self._BASE_MANA}"
