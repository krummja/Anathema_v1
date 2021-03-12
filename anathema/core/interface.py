from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core import Game


class Window:

    selected = 0xFFFF00FF
    unselected = 0xFFFFFFFF

    def __init__(self, x: int, y: int, w: int, h: int, title: str, data, spread: int = 2) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.data = data
        self.spread = spread

    def draw(self, renderer) -> None:
        renderer.draw_box(self.x, self.y, self.w, self.h, 0x44FFFFFF)
        renderer.print(self.x-1, self.y, 0xFFFFFFFF, self.title)
        self.draw_menu_list(renderer)

    def draw_menu_list(self, renderer):
        pass


class InterfaceManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._stack = []

    @property
    def current_window(self):
        if len(self._stack) > 0:
            return self._stack[-1]
