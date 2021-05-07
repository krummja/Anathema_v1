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


class StatLookup(dict):
    STRENGTH = Stat("strength", "STR")
    FINESSE = Stat("finesse", "FIN")
    VITALITY = Stat("vitality", "VIT")
    PIETY = Stat("piety", "PIE")
    CUNNING = Stat("cunning", "CUN")
    KNOWLEDGE = Stat("knowledge", "KNO")


lookup = StatLookup()


def get_stat_name(stat: str) -> str:
    return lookup.get(stat).name


def get_stat_abbr(stat: str) -> str:
    return lookup.get(stat).abbreviation


def get_stat(stat: str, entity: Entity) -> int:
    name = lookup.get(stat).name
    return entity["Stats"][name]()


def roll_stat(stat: str, entity: Entity) -> int:
    roll = randint(1, 20)
    return roll + get_stat(stat, entity)


def stat_check(stat: str, entity: Entity, target: int) -> bool:
    return roll_stat(stat, entity) >= target
