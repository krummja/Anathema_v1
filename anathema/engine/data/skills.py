from __future__ import annotations
from typing import *
import math
from .skill import Skill
from .stats import *

if TYPE_CHECKING:
    from ecstremity import Entity


SKILL_SPEED = "SKILL_SPEED"
SKILL_HEALTH = "SKILL_HEALTH"


class SpeedSkill(Skill):

    def __init__(self):
        super().__init__(SKILL_SPEED, "speed", STAT_VITALITY)

    @staticmethod
    def get_speed_percent(skill: int = 0):
        base = 5
        cost = base / (base + skill)
        return cost

    @staticmethod
    def get_speed_percent_display(skill: int = 0):
        percent = SpeedSkill.get_speed_percent(skill)
        return math.floor(percent * 100)


class SkillRegistry:
    SKILL_SPEED = SpeedSkill()

    def __getitem__(self, key):
        return getattr(self, key)


def get_skill(key: str) -> Skill:
    return SkillRegistry[key]


def get_skill_value(key: str, entity: Entity) -> int:
    return SkillRegistry()[key].compute(entity)
