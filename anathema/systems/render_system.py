from __future__ import annotations

import nocterminal as noc
from anathema.systems.base_system import BaseSystem


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query('tiles', all_of=[ 'Renderable' ], none_of=[ 'Actor' ])
        self.query('actors', all_of=[ 'Actor' ])

    def draw_tiles(self) -> None:
        explored = self.game.fov_system.explored
        visible = self.game.fov_system.visible

        for tile in self._queries['tiles'].result:
            x, y, z = tile['Position'].xyz

            if not explored[x, y]:
                alpha = 0x00000000
            elif explored[x, y] & ~visible[x, y]:
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
            elif explored[x, y] & ~visible[x, y]:
                alpha = 0x66000000
            else:
                alpha = 0xFF000000

            noc.terminal.layer(z)
            noc.terminal.color(alpha + (actor['Renderable'].fore & 0x00FFFFFF))
            noc.terminal.put(x, y, actor['Renderable'].char)

    def update(self, dt) -> None:
        self.game.context.clear()
        self.draw_tiles()
        self.draw_actors()
