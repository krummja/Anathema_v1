from __future__ import annotations
from typing import *
from collections import deque
from functools import reduce
import math

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class FPSManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._fps = 0.0
        self.frames = deque([])
        self.frame_count = 60
        for i in range(self.frame_count-1):
            self.frames.append(0)

    @property
    def fps(self):
        return self._fps / 1000

    def update(self, dt):
        self.frames.append(1000 / dt)
        self.frames.popleft()

        _sum = reduce((lambda s, v: s + v), self.frames, 0)
        self._fps = math.trunc(_sum / self.frame_count)
