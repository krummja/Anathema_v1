from __future__ import annotations

from morphism import *
import nocterminal as noc
from anathema.systems.base_system import BaseSystem


class RenderSystem(BaseSystem):

    viewport: Rect

    def initialize(self):
        self.query('tiles', all_of=[ 'Position' ], none_of=[ 'Actor' ])
        self.query('actors', all_of=[ 'Actor' ])

    def initialize_viewport(self):
        self.viewport = Rect.centered_at(
            Size(96 - 24, 64 - 14),
            Point(*self.game.player.position))

    def draw_tiles(self) -> None:
        explored = self.game.fov_system.explored
        visible = self.game.fov_system.visible

        for tile in self._queries['tiles'].result:
            x, y, z = tile['Position'].xyz

            if not explored[x, y]:
                alpha = 0x00000000
            elif explored[x, y] and not visible[x, y]:
                alpha = 0x66000000
            else:
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
        return (x < self.viewport.width &
                y < self.viewport.height &
                x >= self.viewport.x &
                y >= self.viewport.y)

    def update(self, dt) -> None:
        self.game.context.clear()
        self.draw_tiles()
        self.draw_actors()
