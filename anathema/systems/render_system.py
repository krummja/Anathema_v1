from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.core.options import Options
from anathema.utils.geometry import Rect
from anathema.abstracts import AbstractSystem

if TYPE_CHECKING:
    from anathema.core import Game


class RenderSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.terminal = game.renderer.terminal
        self._tiles = self.ecs.create_query(
            all_of=[ 'Renderable' ],
            none_of=[ 'Actor', 'Item' ])

        self._actors = self.ecs.create_query(
            all_of=[ 'Actor' ])

        self._items = self.ecs.create_query(
            all_of=[ 'Item' ])

    def draw_tiles(self, dt) -> None:
        for tile in self._tiles.result:
            x, y, z = tile['Position'].xyz

            if not self.game.fov_system.explored[x, y]:
                alpha = 0x00000000
            elif (self.game.fov_system.explored[x, y] and
                not self.game.fov_system.visible[x, y]):
                alpha = 0x66000000
            else:
                alpha = 0xFF000000

            if tile['Renderable'].back is not None:
                back = alpha + tile['Renderable'].back
                self.game.renderer.fill_area(x, y, 1, 1, color=back)

            self.terminal.layer(z)
            self.terminal.color(alpha + tile['Renderable'].fore)
            self.terminal.put(x, y, tile['Renderable'].char)

    def draw_items(self, dt) -> None:
        for item in self._items.result:
            x, y, z = item['Position'].xyz

            if not self.game.fov_system.explored[x, y]:
                alpha = 0x00000000
            elif (self.game.fov_system.explored[x, y] and
                not self.game.fov_system.visible[x, y]):
                alpha = 0x66000000
            else:
                alpha = 0xFF000000

            if item['Renderable'].back is not None:
                back = alpha + item['Renderable'].back
                self.game.renderer.fill_area(x, y, 1, 1, color=back)

            self.terminal.layer(z)
            self.terminal.color(alpha + item['Renderable'].fore)
            self.terminal.put(x, y, item['Renderable'].char)

    def draw_actors(self, dt) -> None:
        for actor in self._actors.result:
            x, y, z = actor['Position'].xyz
            self.terminal.clear_area(x, y, 1, 1)
            self.terminal.layer(z)
            self.terminal.color(actor['Renderable'].fore)
            self.terminal.put(x, y, actor['Renderable'].char)

    def update(self, dt) -> None:
        self.terminal.clear()
        self.game.renderer.push_to_stack(self.draw_tiles)
        self.game.renderer.push_to_stack(self.draw_actors)
        self.game.renderer.push_to_stack(self.draw_items)
