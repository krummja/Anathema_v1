from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.abstracts import AbstractSystem
from clubsandwich.geom import Rect, Point, Size

if TYPE_CHECKING:
    from anathema.core import Game


class RenderSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.terminal = game.renderer.terminal
        self.tiles = game.world.current_area.tiles
        self._tiles = self.ecs.create_query(
            all_of=[ 'Renderable' ],
            none_of=[ 'Actor', 'Item' ])

        self._actors = self.ecs.create_query(
            all_of=[ 'Actor' ])

    def render_tiles(self) -> None:
        for tile in self._tiles.result:
            x, y, z = tile['Position'].xyz
            self.terminal.layer(z.value)
            alpha = 0xFF000000 - (0x11000000 * z.value)
            if alpha <= 0x00000000:
                alpha = 0x00000000
            self.terminal.color(alpha + tile['Renderable'].fore)
            self.terminal.put(x, y, tile['Renderable'].char)

    def render_actors(self) -> None:
        for actor in self._actors.result:
            x, y, z = actor['Position'].xyz

            # self.terminal.clear_area(x, y, 1, 1)
            self.terminal.clear_area(Rect(Point(x, y), Size(1, 1)))

            self.terminal.layer(z)
            self.terminal.color(actor['Renderable'].fore)
            self.terminal.put(x, y, actor['Renderable'].char)

    def render(self) -> None:

        self.terminal.clear()
        self.render_tiles()
        self.render_actors()

    def update(self, dt) -> None:
        self.render()
