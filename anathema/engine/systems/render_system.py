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
        self.game.renderer.render_world_map(self.game.maps.viewer)

    def draw_tiles(self):
        self.game.renderer.render_area_tiles(self.game.maps.current_area)

    def draw_items(self):
        pass

    def draw_actors(self):
        cam_x, cam_y = self.game.camera.camera_pos
        actors = self._queries['actors'].result
        for actor in actors:
            x, y = actor['Position'].xy
            if self.game.maps.current_area.visible[y, x]:
                self.game.console.root.tiles_rgb[["ch", "fg"]][y - cam_y, x - cam_x] = (
                    actor['Renderable'].char,
                    actor['Renderable'].fg
                )

    def draw_path(self):
        cam_x, cam_y = self.game.camera.camera_pos
        pathing = filter((lambda e: e['Actor'].is_pathing), self._queries['actors'].result)
        for e in pathing:
            path = e['Actor'].path
            for point in path:
                x = point[0] - cam_x
                y = point[1] - cam_y
                self.game.console.root.tiles_rgb[["ch", "fg"]][y, x] = (
                    ord("o"),
                    ([255, 0, 0])
                )

    def update(self):
        self.game.console.root.clear()
        self.draw_tiles()
        self.draw_actors()

        if self.game.debug:
            self.draw_path()
