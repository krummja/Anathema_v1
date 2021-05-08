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


MIGHT = Stat("might", "MIG")
FINESSE = Stat("finesse", "FIN")
VITALITY = Stat("vitality", "VIT")
PIETY = Stat("piety", "PIE")
CUNNING = Stat("cunning", "CUN")
KNOWLEDGE = Stat("knowledge", "KNO")


def get_stat_name(stat: Stat) -> str:
    return stat.name


def get_stat_abbr(stat: Stat) -> str:
    return stat.abbreviation


def get_stat(stat: Stat, entity: Entity) -> int:
    name = stat.name
    return entity["Stats"][name]()


def roll_stat(stat: Stat, entity: Entity) -> int:
    roll = randint(1, 20)
    return roll + get_stat(stat, entity)


def stat_check(stat: Stat, entity: Entity, target: int) -> bool:
    return roll_stat(stat, entity) >= target
