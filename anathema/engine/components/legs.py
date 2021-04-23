from __future__ import annotations

from typing import TYPE_CHECKING

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        super().__init__()
        self._leg_count = leg_count
        self.area = self.client.world.current_area

    def on_try_move(self, evt: EntityEvent) -> None:
        if self.area.is_blocked(*evt.data.target):
            pass
        # if self.area.is_blocked(*evt.data.target):
        #     if self.area.is_interactable(*evt.data.target):
        #         self.entity.fire_event('try_interact', evt.data)
        #     else:
        #         # Route Message to LogManager
        #         pass
        else:
            self.update_position(*evt.data.target)
        evt.handle()

    def update_position(self, x: int, y: int) -> None:
        self.entity['Position'].x = x
        self.entity['Position'].y = y
