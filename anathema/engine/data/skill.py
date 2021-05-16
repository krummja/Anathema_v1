from __future__ import annotations
from typing import *
from functools import reduce

from anathema.engine.data.stats import get_stat

if TYPE_CHECKING:
    from ecstremity import Entity
    from engine.data.stats import Stat


class Skill:

    def __init__(self, key: str, name: str, base_stat: Stat) -> None:
        self.key = key
        self.name = name
        self.base_stat = base_stat

    def get_modifiers(self, entity: Entity):
        evt = entity.fire_event("query_skill_mod", {
            "name": self.name,
            "skill": self.key,
            "modifiers": []
        })
        return evt.data.modifiers

    def get_modifier_sum(self, entity: Entity):
        modifiers = self.get_modifiers(entity)
        return reduce(lambda _sum, _cur: _sum + _cur[1], modifiers)

    def compute(self, entity: Entity) -> int:
        base_stat = get_stat(self.base_stat, entity)
        stat = base_stat or 0
        modifier = self.get_modifier_sum(entity)
        return stat + modifier[1]
