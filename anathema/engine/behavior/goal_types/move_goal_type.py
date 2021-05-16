from __future__ import annotations
from typing import *
import logging

from anathema.engine.behavior.goal_action_result import *
from .goal_type import GoalType

if TYPE_CHECKING:
    pass


class MoveGoalType(GoalType):

    name: str = 'Move'

    @staticmethod
    def is_finished(entity: Entity, goal: Component):
        return goal.complete

    @staticmethod
    def take_action(entity: Entity, goal: Component):
        target_x = entity['Position'].x + goal.data[0]
        target_y = entity['Position'].y + goal.data[1]

        evt = entity.fire_event('try_move', {
            "target": (target_x, target_y)
        })

        if evt.handled:
            goal.complete = True
            return SUCCESS
        return FAILURE
