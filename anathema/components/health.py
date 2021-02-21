from __future__ import annotations

from ecstremity import Component


class Health(Component):

    def __init__(self, base: int) -> None:
        self._BASE = base
        self._EXPENDED: int = 0
        self._ALIVE: bool = True    # TODO: Split this off into a separate flag cmp

    @property
    def current(self) -> int:
        return self._BASE - self._EXPENDED

    @property
    def maximum(self) -> int:
        return self._BASE

    def expend(self, value: int) -> None:
        if self._ALIVE:
            self._EXPENDED += value
        if self._EXPENDED == self._BASE:
            self._ALIVE = False

    def recoup(self, value: int) -> None:
        self.expend(value * -1)

    def __str__(self) -> str:
        return f"{self.current}/{self._BASE}"
