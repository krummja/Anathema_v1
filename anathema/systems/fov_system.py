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
        self._pov = self.ecs.create_query(
            all_of=[ 'IsPlayer' ])
        self._query = self.ecs.create_query(
            all_of=[ 'Opacity' ])
        self.transparent = np.ones((64, 64), dtype=np.bool, order="F")
        self.explored = np.zeros((64, 64), dtype=np.bool, order="F")
        self.visible = np.zeros((64, 64), dtype=np.bool, order="F")

    def compute_fov(self):
        self.visible = tcod.map.compute_fov(
            transparency=self.transparent,
            pov=self._pov.result[0]['Position'].xy,
            radius=self._pov.result[0]['Eyes'].vision,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
            )
        self.explored |= self.visible

    def update(self, dt):
        for target in self._query.result:
            x, y = target['Position'].xy
            if target['Opacity'].opaque:
                self.transparent[x][y] = False
            else:
                self.transparent[x][y] = True
        self.compute_fov()
