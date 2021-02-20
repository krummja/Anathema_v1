from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.core.options import Options
from anathema.abstracts import AbstractSystem
from anathema.utils.geometry import Rect
from collections import deque

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

    def draw_tiles(self) -> None:
        for tile in self._tiles.result:
            x, y, z = tile['Position'].xyz

            self.terminal.layer(z.value)
            self.terminal.color(0xFF000000 + tile['Renderable'].fore)
            self.terminal.put(x, y, tile['Renderable'].char)

    def draw_actors(self) -> None:
        for actor in self._actors.result:
            x, y, z = actor['Position'].xyz

            self.terminal.clear_area(x, y, 1, 1)
            self.terminal.layer(z)
            self.terminal.color(actor['Renderable'].fore)
            self.terminal.put(x, y, actor['Renderable'].char)

    def clear_below(self, x, y, z):
        layers = deque([i for i in range(0, z)])
        for layer in layers:
            self.terminal.layer(layer)
            self.terminal.clear_area(x, y, 1, 1)

    def on_draw(self, dt) -> None:
        self.draw_tiles()
        self.draw_actors()

    def update(self, dt) -> None:
        self.on_draw(dt)
