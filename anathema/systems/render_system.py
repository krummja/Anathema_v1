from __future__ import annotations
from typing import *

from morphism import *
import nocterminal as noc
from anathema.systems.base_system import BaseSystem


VIEWPORT_WIDTH = 32
VIEWPORT_HEIGHT = 24


class RenderSystem(BaseSystem):

    _camera_bounds: Rect = None
    _render_offset: Tuple[int, int] = (0, 0)
    bounds: Rect = None

    def initialize(self):
        self.query('tiles', all_of=[ 'Position' ], none_of=[ 'Actor' ])
        self.query('actors', all_of=[ 'Actor' ])
        self.bounds = Rect(Point(0, 0), Size(VIEWPORT_WIDTH, VIEWPORT_HEIGHT))

    def draw_tiles(self) -> None:
        explored = self.game.fov_system.explored
        visible = self.game.fov_system.visible

        for tile in self._queries['tiles'].result:
            x, y, z = tile['Position'].xyz

            # if not explored[x, y]:
            #     alpha = 0x00000000
            # elif explored[x, y] and not visible[x, y]:
            #     alpha = 0x66000000
            # else:
            #     alpha = 0xFF000000

            alpha = 0xFF000000

            noc.terminal.layer(0)
            noc.terminal.color(alpha + (tile['Renderable'].back & 0x00FFFFFF))
            noc.terminal.put(x, y, "█")

            noc.terminal.layer(z)
            noc.terminal.color(alpha + (tile['Renderable'].fore & 0x00FFFFFF))
            noc.terminal.put(x, y, tile['Renderable'].char)

    def draw_actors(self) -> None:
        explored = self.game.fov_system.explored
        visible = self.game.fov_system.visible

        for actor in self._queries['actors'].result:
            x, y, z = actor['Position'].xyz

            if not explored[x, y]:
                alpha = 0x00000000
            elif explored[x, y] and not visible[x, y]:
                alpha = 0x66000000
            else:
                alpha = 0xFF000000

            noc.terminal.layer(z)
            noc.terminal.color(alpha + (actor['Renderable'].fore & 0x00FFFFFF))
            noc.terminal.put(x, y, actor['Renderable'].char)

    def is_in_view(self, x, y):
        return (0 <= x < self._camera_bounds.width,
                0 <= y < self._camera_bounds.height)

    def update(self, dt) -> None:
        self.game.context.clear()
        # self._position_camera()
        self.draw_tiles()
        self.draw_actors()

    def _position_camera(self):
        pov = self.game.player.position
        range_width = max(0, 128 - VIEWPORT_WIDTH)
        range_height = max(0, 128 - VIEWPORT_HEIGHT)
        camera_range = Rect(Point(0, 0), Size(range_width, range_height))

        camera = (min(camera_range.x, max(pov[0], camera_range.width)),
                  min(camera_range.y, max(pov[1], camera_range.height)))

        self._camera_bounds = Rect(Point(camera[0], camera[1]),
                                   Size(min(VIEWPORT_WIDTH, 128), min(VIEWPORT_HEIGHT, 128)))

        self._render_offset = (max(0, VIEWPORT_WIDTH - 128) % 2, max(0, VIEWPORT_HEIGHT - 128))
