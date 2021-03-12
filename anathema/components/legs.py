from __future__ import annotations
from typing import TYPE_CHECKING

from .bases.body_part import BodyPart

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Legs(BodyPart):

    def __init__(self, leg_count: int = 2) -> None:
        super().__init__()
        self._leg_count = leg_count

    def on_try_move(self, evt: EntityEvent) -> None:
        self.update_position(*evt.data['target'])
        evt.handle()

    def update_position(self, x: int, y: int) -> None:
        self.entity['Position'].x = x
        self.entity['Position'].y = y
