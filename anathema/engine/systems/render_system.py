from __future__ import annotations
from typing import *

from anathema.engine.core.options import Options
from anathema.engine.systems import BaseSystem

if TYPE_CHECKING:
    pass


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query('actors', all_of=[ 'Actor', 'Renderable' ])

    def draw_world_map(self):
        self.game.console.root.clear()
        self.game.renderer.render_world_map(self.game.world.planet_view)

    def draw_tiles(self):
        self.game.renderer.render_area_tiles(self.game.world.current_area)

    def draw_items(self):
        pass

    def draw_actors(self):
        cam_x, cam_y = self.game.camera.camera_pos
        actors = self._queries['actors'].result
        for actor in actors:
            x, y = actor['Position'].xy
            x -= cam_x
            y -= cam_y

            self.game.console.root.tiles_rgb[["ch", "fg"]][y, x] = (
                actor['Renderable'].char,
                actor['Renderable'].fg
            )

    def update(self):
        self.game.console.root.clear()
        self.draw_tiles()
        self.draw_actors()