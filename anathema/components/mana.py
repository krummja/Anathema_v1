from __future__ import annotations

from .bases.core_stat import CoreStat


class Mana(CoreStat):

    def __init__(self, base: int) -> None:
        super().__init__(base)
