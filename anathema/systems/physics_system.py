from __future__ import annotations
from typing import TYPE_CHECKING, List

import numpy as np
from ecstremity import Entity

from anathema.systems.system import AbstractSystem


if TYPE_CHECKING:
    from anathema.core.game import Game


class PhysicsSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._blockers = self.ecs.create_query(
            all_of=[ 'Blocker' ])

        self._entities = self.ecs.create_query(
            all_of=[ 'Position' ],
            none_of=[ 'IsInventoried', 'IsDestroying' ])

        self.passable = np.ones((64, 64), dtype=np.bool, order="F")

    def entity_at_pos(self, x: int, y: int) -> List[Entity]:
        entities = []
        for target in self._entities.result:
            if target['Position'].xy == (x, y):
                entities.append(target.uid)
        return entities

    def update(self, dt):
        for target in self._blockers.result:
            x, y = target['Position'].xy
            if target.has('Blocker'):
                self.passable[x][y] = False
            else:
                self.passable[x][y] = True
