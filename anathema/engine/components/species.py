from __future__ import annotations
from typing import *

from ecstremity import Component

from anathema.engine.data.species import get_species_data
from anathema.engine.data.species_data import SpeciesData
from anathema.engine.data.skills import SKILL_SPEED

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Species(Component):

    def __init__(self, key: str):
        self.key = key

    @property
    def data(self) -> SpeciesData:
        return get_species_data(self.key)

    @property
    def name(self):
        return self.data.name

    @property
    def speed(self):
        return self.data.speed

    def get_modifier(self, stat: str):
        return self.data[stat]

    def on_query_stat_mod(self, evt: EntityEvent) -> None:
        mod = self.get_modifier(evt.data.stat)
        if mod != 0:
            evt.data.modifiers.append((self.name, mod))

    def on_query_skill_mod(self, evt: EntityEvent) -> None:
        if evt.data.skill == SKILL_SPEED:
            mod = self.speed
            evt.data.modifiers.append((self.name, mod))
