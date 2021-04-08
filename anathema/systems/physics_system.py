from __future__ import annotations
from typing import List

import numpy as np
from ecstremity import Entity

from anathema.systems.base_system import BaseSystem


class PhysicsSystem(BaseSystem):

    passable = np.ones((64, 64), dtype=bool, order="F")

    def initialize(self):
        self.query('blockers', all_of=[ 'Blocker' ])
        self.query('entities', all_of=[ 'Position' ], none_of=[ 'IsInventoried' ])

    def entity_at_pos(self, x: int, y: int) -> List[Entity]:
        entities = []
        for target in self._queries['entities'].result:
            if target['Position'].xy == (x, y):
                entities.append(target.uid)
        return entities

    def update(self, dt):
        for target in self._queries['blockers'].result:
            x, y = target['Position'].xy
            if target.has('Blocker'):
                self.passable[x][y] = False
            else:
                self.passable[x][y] = True
