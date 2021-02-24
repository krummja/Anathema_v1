from __future__ import annotations

from ecstremity import Component
from .bases.core_stat import CoreStat


class Health(CoreStat):

    _removable: bool = False

    def __init__(self, base: int) -> None:
        super().__init__(base)
        self._ALIVE: bool = True    # TODO: Split this off into a separate flag cmp

    def expend(self, value: int) -> None:
        if self._ALIVE:
            self._EXPENDED += value
        if self._EXPENDED == self._BASE:
            self._ALIVE = False
