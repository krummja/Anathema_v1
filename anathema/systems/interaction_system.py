from __future__ import annotations
from typing import TYPE_CHECKING
from ecstremity.entity import Entity

import numpy as np

from anathema.abstracts import AbstractSystem


if TYPE_CHECKING:
    from anathema.core.game import Game


class InteractionSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._interactables = self.ecs.create_query(
            all_of=[ 'IsInteractable' ])
        self._statics = self.ecs.create_query(
            all_of=[ 'IsStatic' ])
        self.interactable = np.zeros((64, 64), dtype=np.bool, order="F")

    def update(self, dt):
        for interactable in self._interactables.result:
            x, y = interactable['Position'].xy
            self.interactable[x][y] = True
        for static in self._statics.result:
            x, y = static['Position'].xy
            self.interactable[x][y] = False

    def get_interactables_at_pos(self, x: int, y: int) -> str:
        for interactable in self._interactables.result:
            if interactable.has('Position') and interactable['Position'].xy == (x, y):
                return interactable
