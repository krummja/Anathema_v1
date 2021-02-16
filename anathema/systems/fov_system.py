from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import tcod

from anathema.abstracts import AbstractSystem

if TYPE_CHECKING:
    from anathema.core.game import Game


class FOVSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=[ 'IsPlayer' ])
        self._opaque = self.ecs.create_query(
            all_of=[ 'Opaque' ])
        self.transparent = np.ones((64, 64), dtype=np.bool, order="F")
        self.explored = np.zeros((64, 64), dtype=np.bool, order="F")
        self.visible = np.zeros((64, 64), dtype=np.bool, order="F")

    def update_fov(self) -> None:
        for opaque in self._opaque.result:
            x, y = opaque['Position'].xy
            self.transparent[x][y] = False

        self.visible = tcod.map.compute_fov(
            transparency=self.transparent,
            pov=self._query.result[0]['POSITION'].xy,
            radius=8,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
            )
        self.explored |= self.visible

    def update(self, dt):
        self.update_fov()