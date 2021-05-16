from __future__ import annotations
from typing import *
from random import randint
from dataclasses import dataclass

if TYPE_CHECKING:
    from ecstremity import Entity


@dataclass
class Stat:
    name: str
    abbreviation: str


STAT_MIGHT = Stat("might", "MIG")
STAT_FINESSE = Stat("finesse", "FIN")
STAT_VITALITY = Stat("vitality", "VIT")
STAT_PIETY = Stat("piety", "PIE")
STAT_CUNNING = Stat("cunning", "CUN")
STAT_KNOWLEDGE = Stat("knowledge", "KNO")


def get_stat_name(stat: Stat) -> str:
    return stat.name


def get_stat_abbr(stat: Stat) -> str:
    return stat.abbreviation


def get_stat(stat: Stat, entity: Entity) -> int:
    name = stat.name
    return entity["Stats"][name]


def roll_stat(stat: Stat, entity: Entity) -> int:
    roll = randint(1, 20)
    return roll + get_stat(stat, entity)


def stat_check(stat: Stat, entity: Entity, target: int) -> bool:
    return roll_stat(stat, entity) >= target
