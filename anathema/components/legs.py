from __future__ import annotations

from ecstremity import Component


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        self._leg_count = leg_count

    def on_try_move(self, evt):
        success = evt.data[0]
        direction = evt.data[1][0]

        if success:
            self.update_position(*direction)
            evt.handle()
        else:
            evt.prevent()

    def update_position(self, x, y):
        pos_x, pos_y = self.entity['Position'].xy
        target_x = pos_x + x
        target_y = pos_y + y
        self.entity['Position'].x = target_x
        self.entity['Position'].y = target_y
