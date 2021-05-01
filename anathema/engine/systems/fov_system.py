from __future__ import annotations
from typing import *
import tcod

from anathema.engine.systems import BaseSystem

if TYPE_CHECKING:
    pass


class FOVSystem(BaseSystem):

    def initialize(self):
        self.query('pov', all_of=[ 'IsPlayer' ])

    def update_fov(self):
        self.game.world.current_area.visible = tcod.map.compute_fov(
            transparency=self.game.world.current_area.tiles["transparent"],
            pov=self._queries['pov'].result[0]['Position'].ij,
            radius=12,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
        )
        self.game.world.current_area.explored |= self.game.world.current_area.visible

    def update(self):
        self.game.camera.camera_pos = self._queries['pov'].result[0]['Position'].xy
        self.update_fov()
