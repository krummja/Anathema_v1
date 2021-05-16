from __future__ import annotations
from typing import *

from anathema.engine.behavior.goal_action_result import *
from .goal_type import GoalType
from .kill_something_goal_type import KillSomethingGoalType

if TYPE_CHECKING:
    from ecstremity import Engine, Entity


class BoredGoalType(GoalType):

    name: str = 'Bored'

    @staticmethod
    def is_finished(entity: Entity, goal: Component):
        return False

    @staticmethod
    def take_action(entity: Entity, goal: Component):

        kill_event = entity.fire_event('try_detect_hostiles', {
            "targets": set()
        })

        if len(kill_event.data.targets) > 0:
            target = kill_event.data.targets[0]
            kill_goal = KillSomethingGoalType().create_sub_goal(
                entity.world, goal, { "target": target }
            )

            entity["Brain"].append_goal(kill_goal)
            entity.fire_event('take_action')
            return SUCCESS

        bored_event = entity.fire_event('boredom')
        try:
            if bored_event.data.goal:
                entity["Brain"].append_goal(bored_event.data.goal)
                entity.fire_event("take_action")
                return SUCCESS
        except AttributeError:
            entity.fire_event("energy_consumed", {"cost": 1000})
            return SUCCESS
