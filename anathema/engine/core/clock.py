from __future__ import annotations
from typing import *
import math
import logging

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class ClockManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._tick: int = 0
        self._tick_delta: int = 0
        self._turn_delta: int = 0

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def tick_delta(self) -> int:
        return self._tick_delta

    @property
    def turn_delta(self) -> int:
        return self._turn_delta

    @property
    def turn(self) -> int:
        return math.floor(self._tick / 1000)

    @property
    def subturn(self) -> int:
        return self._tick - self.turn * 1000

    def increment(self, delta):
        prev_turn = self.turn
        self._tick_delta = delta
        self._tick += delta
        curr_turn = self.turn
        self._turn_delta = curr_turn - prev_turn

    def update(self):
        self._tick_delta = 0
        self._turn_delta = 0
