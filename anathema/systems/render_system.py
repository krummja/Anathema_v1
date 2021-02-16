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

        self._statics = self.ecs.create_query(
            all_of=[ 'Renderable' ],
            none_of=[ 'Actor' ])
        self._actors = self.ecs.create_query(
            all_of=[ 'Renderable', 'Actor' ])

    def draw(self) -> None:
        for static in self._statics.result:
            position = static['Position'].xy
            if self.game.fov_system.visible[position[0], position[1]]:
                self.draw_visible(at=position, renderable=static['Renderable'])
            elif self.game.fov_system.explored[position[0], position[1]]:
                self.draw_explored(at=position, renderable=static['Renderable'])
            else:
                self.terminal.layer(20)
                self.terminal.color(0xFF2A2A2A)
                self.terminal.put(*position, "█")

        for actor in self._actors.result:
            position = actor['Position'].xy
            if self.game.fov_system.visible[position[0], position[1]]:
                self.draw_actor(at=position, renderable=actor['Renderable'])

    def draw_visible(self, *, at, renderable) -> None:
        self.terminal.layer(1)
        self.terminal.color(renderable.fore)
        self.terminal.put(*at, renderable.char)

    def draw_explored(self, *, at, renderable) -> None:
        self.terminal.layer(1)
        self.terminal.color(0x88888888)
        self.terminal.put(*at, renderable.char)

    def draw_actor(self, *, at, renderable) -> None:
        self.terminal.layer(1)
        self.terminal.clear_area(*at, 1, 1)
        self.terminal.layer(2)
        self.terminal.color(renderable.fore)
        self.terminal.put(*at, renderable.char)

    def render(self) -> None:
        self.terminal.clear()
        self.draw()

    def update(self, dt) -> None:
        self.render()
