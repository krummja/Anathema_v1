from __future__ import annotations
from typing import *
from dataclasses import dataclass
from anathema.engine.core.options import Options


CIVILIZATIONS = 4
TRIBES = 10
MIN_RIVER_LENGTH = 3
CIV_MAX_SITES = 20
EXPANSION_DISTANCE = 10
WAR_DISTANCE = 8


class Tile:

    has_river = False
    is_civ = False
    biome_id = 0
    prosperity = 0

    def __init__(self, height, temp, precip, drain, biome):
        self.height = height
        self.temp = temp
        self.precip = precip
        self.drain = drain
        self.biome = biome


@dataclass
class Culture:
    name = ""
    biome = None
    strength = None
    size = None
    fertility = None
    aggression = None
    form = None

    def __str__(self):
        return self.name


@dataclass
class CivSite:
    x: int
    y: int
    category = None
    suitable = None
    population_cap = None
    _population = 0
    _is_capital = False


@dataclass
class Army:
    x: int
    y: int
    civilization: Civilization
    size: int


@dataclass
class Civilization:
    name = ""
    culture: Culture
    government: Government
    color: Tuple[int, int, int]
    flag = None
    _sites = []
    _suitable_sites = []
    _is_at_war = False
    _army = None
    _population = 0

    @property
    def aggression(self):
        return self.aggression + self.government.aggression

    def __str__(self):
        return f"the {self.culture} {self.government} of {self.name}"


@dataclass
class Government:
    name: str
    description: str
    aggression = None
    militarization = None
    tech_bonus = None

    def __str__(self):
        return self.name


@dataclass
class War:
    side_a = None
    side_b = None
