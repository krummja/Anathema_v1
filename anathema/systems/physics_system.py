from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from anathema.abstracts import AbstractSystem


if TYPE_CHECKING:
    from anathema.core.game import Game


class PhysicsSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=[ 'Blocker' ])
        self.passable = np.ones((64, 64), dtype=np.bool, order="F")

    def update(self, dt):
        for target in self._query.result:
            x, y = target['Position'].xy
            if target.has('Blocker'):
                self.passable[x][y] = False
            else:
                self.passable[x][y] = True
