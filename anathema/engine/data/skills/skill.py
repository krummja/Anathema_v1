from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity import Entity
    from ..stats import Stat


class Skill:

    def __init__(self, key: int, name: str, base_stat: Stat) -> None:
        self.key = key
        self.name = name
        self.base_stat = base_stat

    @staticmethod
    def get_modifiers(entity: Entity):
        evt = entity.fire_event("query_skill_mod", {
            "name": self.name,
            "skill": self.key,
            "modifiers": []
        })
        return evt.data

    @staticmethod
    def get_modifier_sum(entity: Entity):
        pass

    @staticmethod
    def compute(entity: Entity):
        pass
