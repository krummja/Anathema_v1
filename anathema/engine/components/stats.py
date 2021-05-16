from __future__ import annotations
from typing import *
from functools import reduce

from ecstremity import Component
from anathema.engine.data.stats import (
    STAT_MIGHT,
    STAT_FINESSE,
    STAT_VITALITY,
    STAT_PIETY,
    STAT_CUNNING,
    STAT_KNOWLEDGE,
    get_stat_name,
    get_stat_abbr
)

if TYPE_CHECKING:
    from anathema.engine.data.stats import Stat


def sum_modifiers(modifiers):
    return reduce(lambda _sum, _cur: _sum + _cur.mod, modifiers)


class Stats(Component):

    def __init__(
            self,
            base_might: int,
            base_finesse: int,
            base_vitality: int,
            base_piety: int,
            base_cunning: int,
            base_knowledge: int,
        ) -> None:
        self.base_might = base_might
        self.base_finesse = base_finesse
        self.base_vitality = base_vitality
        self.base_piety = base_piety
        self.base_cunning = base_cunning
        self.base_knowledge = base_knowledge

    def get_stat_modifiers(self, stat: Stat):
        evt = self.entity.fire_event('query_stat_mod', {
            "name": get_stat_name(stat),
            "stat": stat,
            "modifiers": []
        })
        return evt.data.modifiers

    def get_stat_modifier_sum(self, stat: Stat):
        mods = self.get_stat_modifiers(stat)
        return sum_modifiers(mods)

    def data(self, stat: Stat) -> Dict[str, Any]:
        base = getattr(self, f"base_{stat.name}")
        modifiers = self.get_stat_modifiers(stat)
        mod_sum = sum_modifiers(modifiers)

        return {
            "stat": Stat,
            "name": get_stat_name(stat),
            "abbreviation": get_stat_abbr(stat),
            "modifiers": modifiers,
            "base": base,
            "mod_sum": mod_sum,
            "sum": base + mod_sum
        }

    def get_all(self):
        return {
            "might": self.data(STAT_MIGHT),
            "finesse": self.data(STAT_FINESSE),
            "vitality": self.data(STAT_VITALITY),
            "piety": self.data(STAT_PIETY),
            "cunning": self.data(STAT_CUNNING),
            "knowledge": self.data(STAT_KNOWLEDGE),
        }

    def might(self):
        mod = self.get_stat_modifier_sum(STAT_MIGHT)
        return self.base_might + mod[1]

    def finesse(self):
        mod = self.get_stat_modifier_sum(STAT_FINESSE)
        return self.base_finesse + mod[1]

    def vitality(self):
        mod = self.get_stat_modifier_sum(STAT_VITALITY)
        return self.base_vitality + mod[1]

    def piety(self):
        mod = self.get_stat_modifier_sum(STAT_PIETY)
        return self.base_piety + mod[1]

    def cunning(self):
        mod = self.get_stat_modifier_sum(STAT_CUNNING)
        return self.base_cunning + mod[1]

    def knowledge(self):
        mod = self.get_stat_modifier_sum(STAT_KNOWLEDGE)
        return self.base_knowledge + mod[1]

    def __getitem__(self, key: str):
        if key in ["might", "finesse", "vitality", "piety", "cunning", "knowledge"]:
            stat = getattr(self, key)
            return stat()
