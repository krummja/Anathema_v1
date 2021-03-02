from __future__ import annotations

from .bases.body_part import BodyPart

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .body import Body


class Legs(BodyPart):

    def __init__(self, leg_count: int = 2) -> None:
        super().__init__()
        self._leg_count = leg_count

    def on_try_move(self, evt):

        if evt.data.success:
            self.update_position(*evt.data.require['to'])
            evt.handle()
        else:
            self.ecs.client.log.log.report(evt.data.result)
            evt.prevent()

    def update_position(self, x, y):
        pos_x, pos_y = self.entity['Position'].xy
        target_x = pos_x + x
        target_y = pos_y + y
        self.entity['Position'].x = target_x
        self.entity['Position'].y = target_y
