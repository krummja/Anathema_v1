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
        player = self._queries['pov'].result[0]
        self.game.maps.current_area.visible = tcod.map.compute_fov(
            transparency=self.game.maps.current_area.tiles["transparent"],
            pov=player['Position'].ij,
            radius=player['Eyes'].sight_range,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE
        )
        self.game.maps.current_area.explored |= self.game.maps.current_area.visible

    def update(self):
        self.game.camera.camera_pos = self._queries['pov'].result[0]['Position'].xy
        self.update_fov()
