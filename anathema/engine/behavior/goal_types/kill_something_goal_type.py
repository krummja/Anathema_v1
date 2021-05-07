from __future__ import annotations
from typing import *
import tcod
import numpy as np
# from ecstremity import EventData

from anathema.engine.behavior.goal_action_result import *
from anathema.engine.data.directions import direction_delta
from .goal_type import GoalType
from .move_goal_type import MoveGoalType

if TYPE_CHECKING:
    from anathema.engine.world.area import Area
    from ecstremity import Engine, Entity


class KillSomethingGoalType(GoalType):

    name: str = 'KillSomething'

    @staticmethod
    def is_finished(entity: Entity, goal: Component):
        return not goal.target or goal.target.is_destroyed

    @staticmethod
    def take_action(entity: Entity, goal: Component):
        # evt = entity.fire_event('try_melee', EventData(
        #     target = goal.target
        # ))
        #
        # if evt.data.success:
        #     return SUCCESS

        target_pos = goal.target['Position'].xy
        entity['Actor'].is_pathing = True
        entity['Actor'].dest_xy = target_pos
        entity.world.engine.client.path_system.update()

        if len(entity['Actor'].path) > 0:
            start_position = entity["Position"].xy
            next_position = entity["Actor"].path[0]

            delta = (next_position[0] - start_position[0],
                     next_position[1] - start_position[1])

            entity['Brain'].append_goal(MoveGoalType().create_sub_goal(
                entity.world, goal, { "data": delta }
            ))

            entity.fire_event('take_action')
            return SUCCESS

        entity['Actor'].is_pathing = False
        entity.fire_event('energy_consumed', {"cost": 1000})
        return FAILURE
