from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from anathema.abstracts import AbstractSystem

if TYPE_CHECKING:
    from anathema.core import Game


class RenderSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.terminal = game.renderer.terminal

        self._query = self.ecs.create_query(
            all_of=[ 'Renderable' ])

    def draw_tiles(self) -> None:
        self.terminal.layer(1)
        for tile in self._query.result:
            position = tile['Position'].xy
            self.terminal.color(tile['Renderable'].fore)
            self.terminal.put(*position, tile['Renderable'].char)

    def render(self) -> None:
        self.terminal.clear()
        self.draw_tiles()

    def update(self, dt) -> None:
        self.render()
