from __future__ import annotations
from typing import *
from math import floor
from random import randint, random
from ecstremity import Component, EntityEvent

from anathema.engine.data.directions import direction_delta
from anathema.engine.behavior.goal_types.move_goal_type import MoveGoalType

if TYPE_CHECKING:
    pass


class Wandering(Component):

    def on_boredom(self, evt: EntityEvent):
        if randint(0, 100) > 50:
            return
        direction = floor(random() * 9)
        delta = direction_delta(direction)
        evt.data = {"goal": MoveGoalType().create(self.world, {"data": delta})}
        evt.handle()
