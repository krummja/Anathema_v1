from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from anathema.engine.data.stats import Stat


class SpeciesData:

    def __init__(
            self,
            name: str = "",
            speed: int = 1,
            base_might: int = 0,
            base_finesse: int = 0,
            base_vitality: int = 0,
            base_piety: int = 0,
            base_cunning: int = 0,
            base_knowledge: int = 0,
        ) -> None:
        self.name: str = name
        self.speed: int = speed
        self.base_might: int = base_might
        self.base_finesse: int = base_finesse
        self.base_vitality: int = base_vitality
        self.base_piety: int = base_piety
        self.base_cunning: int = base_cunning
        self.base_knowledge: int = base_knowledge

    def __getitem__(self, key: str):
        return getattr(self, "base_" + key.name)
