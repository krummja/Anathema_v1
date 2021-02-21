from __future__ import annotations
from typing import TYPE_CHECKING

from collections import deque
from clubsandwich.blt.nice_terminal import terminal

from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class RenderManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._terminal = terminal
        self._stack = deque([])

    @property
    def terminal(self) -> terminal:
        return self._terminal

    def refresh(self) -> None:
        self._terminal.refresh()

    def clear(self) -> None:
        self._terminal.clear()
        self._terminal.bkcolor(0xFF2A2A2A)

    def setup(self) -> None:
        self._terminal.open()
        self._terminal.composition(True)
        self._terminal.bkcolor(0xFF2A2A2A)

    def teardown(self) -> None:
        self._terminal.composition(False)
        self._terminal.close()

    def fill(self, char: str = "█", color: int = 0xFF2A2A2A) -> None:
        self._terminal.layer(0)
        self._terminal.color(color)
        for x in range(96):
            for y in range(64):
                self._terminal.put(x, y, char)

    def push_to_stack(self, func) -> None:
        self._stack.append(func)

    def clear_stack(self) -> None:
        self._stack.clear()

    def update(self, dt) -> None:
        while len(self._stack) > 0:
            draw = self._stack.popleft()
            draw(dt)
        self._terminal.refresh()
        self.clear_stack()

    def print(self, x, y, color, string):
        self.terminal.layer(100)
        self.terminal.color(color)
        self.terminal.print(x, y, string)

    def draw_box(self, x, y, w, h, color):
        # upper border
        self.terminal.layer(100)
        self.terminal.color(color)
        border = '┌' + '─' * (w) + '┐'
        self.terminal.print(x - 1, y - 1, border)
        # sides
        for i in range(h):
            self.terminal.print(x - 1, y + i, '│')
            self.terminal.print(x + w, y + i, '│')
        # lower border
        border = '└' + '─' * (w) + '┘'
        self.terminal.print(x - 1, y + h, border)
