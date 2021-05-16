from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from ecstremity import Component

from anathema.engine.data.skills import get_skill_value, SKILL_SPEED

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        self.leg_count = leg_count

    def on_try_move(self, evt: EntityEvent) -> None:
        if self.client.world.current_area.is_blocked(*evt.data.target):
            pass
        # if self.area.is_blocked(*evt.data.target):
        #     if self.area.is_interactable(*evt.data.target):
        #         self.entity.fire_event('try_interact', evt.data)
        #     else:
        #         # Route Message to LogManager
        #         pass
        else:
            speed = get_skill_value(SKILL_SPEED, self.entity)
            cost = (20 / (20 + speed)) * 1000
            evt.data.cost = cost
            self.entity.fire_event('energy_consumed', evt.data)
            self.update_position(*evt.data.target)
            evt.handle()

    def update_position(self, x: int, y: int) -> None:
        self.entity['Position'].xy = x, y
