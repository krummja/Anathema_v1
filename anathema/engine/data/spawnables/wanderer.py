from __future__ import annotations
from typing import *

from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType
from anathema.main import game


def create_spawnable():
    wanderer = game.ecs.world.create_prefab("Wanderer", {
        "Position"
    })
    wanderer["Brain"].append_goal(BoredGoalType())
    return wanderer
