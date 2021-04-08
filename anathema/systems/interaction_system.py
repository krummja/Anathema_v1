from __future__ import annotations
from typing import List
from ecstremity.entity import Entity
from morphism import Circ, Point

import numpy as np

from anathema.systems.base_system import BaseSystem


class InteractionSystem(BaseSystem):

    interactable = np.zeros((64, 64), dtype=bool, order="F")

    def initialize(self):
        self.query('instigator', all_of=[ 'IsPlayer' ])
        self.query('interactables', all_of=[ 'IsInteractable' ], none_of=[ 'IsInventoried' ])

    def update(self, dt):
        for interactable in self._queries['interactables'].result:
            x, y = interactable['Position'].xy
            self.interactable[x][y] = True

    def get(self, x: int, y: int) -> Entity:
        for interactable in self._queries['interactables'].result:
            if interactable.has('Position') and interactable['Position'].xy == (x, y):
                return interactable

    def get_nearby_interactables(self) -> List[Entity]:
        nearby = []
        origin = Point(*self._queries['instigator'].result[0]['Position'].xy)
        reach = Circ.centered_at(radius=3, center=origin)
        for interactable in self._queries['instigator'].result:
            if interactable.has('Position'):
                position = Point(*interactable['Position'].xy)
                if reach.intersects(position):
                    nearby.append(interactable)
        return nearby
