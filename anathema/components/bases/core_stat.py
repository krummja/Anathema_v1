from __future__ import annotations

from ecstremity import Component


class CoreStat(Component):

    def __init__(self, base: int) -> None:
        self._BASE = base
        self._EXPENDED: int = 0

    @property
    def current(self) -> int:
        return self._BASE - self._EXPENDED

    @property
    def maximum(self) -> int:
        return self._BASE

    def expend(self, value: int) -> None:
        self._EXPENDED += value

    def recoup(self, value: int) -> None:
        self.expend(value * -1)

    def __str__(self) -> str:
        return f"{self.current}/{self.maximum}"
