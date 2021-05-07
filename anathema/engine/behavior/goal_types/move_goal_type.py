from __future__ import annotations
from typing import *
from ecstremity import EventData

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

        evt = entity.fire_event('try_move', EventData(
            target = (target_x, target_y)
        ))

        if evt.handled:
            goal.complete = True
            if entity['Actor'].is_pathing:
                if not entity['Actor'].path:
                    entity['Actor'].is_pathing = False
            return SUCCESS
        return FAILURE