from __future__ import annotations
from anathema.components import *

import numpy as np
import tcod

from anathema.systems.base_system import BaseSystem


class FOVSystem(BaseSystem):
    transparent = np.ones((64, 64), dtype=bool, order="F")
    explored = np.zeros((64, 64), dtype=bool, order="F")
    visible = np.zeros((64, 64), dtype=bool, order="F")

    def initialize(self):
        self.query('pov', all_of=[ IsPlayer ])
        self.query('opaque', all_of=[ IsOpaque ])

    def compute_fov(self):

        self.visible = tcod.map.compute_fov(
            transparency=self.transparent,
            pov=self._queries['pov'].result[0]['Position'].xy,
            radius=self._queries['pov'].result[0]['Eyes'].vision,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
            )
        self.explored |= self.visible

    def update(self, dt):
        for target in self._queries['opaque'].result:
            x, y = target['Position'].xy
            if target.has(IsOpaque):
                self.transparent[x][y] = False
            else:
                self.transparent[x][y] = True
        self.compute_fov()
