from __future__ import annotations
from typing import TYPE_CHECKING

import math
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
        self._terminal.bkcolor(0xFF151515)

    def clear_area(self, x: int, y: int, w: int, h: int) -> None:
        self._terminal.clear_area(x-1, y-1, w, h)

    def setup(self) -> None:
        self._terminal.open()
        self._terminal.composition(True)
        self._terminal.bkcolor(0xFF151515)

    def teardown(self) -> None:
        self._terminal.composition(False)
        self._terminal.close()

    def fill_area(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            char: str = "█",
            color: int = 0xFF151515,
            layer: int = 0
        ) -> None:
        self._terminal.layer(layer)
        self._terminal.color(color)
        for _x in range(x, x + width):
            for _y in range(y, y + height):
                self._terminal.put(_x, _y, char)

    def fill(self, char: str = "█", color: int = 0xFF151515) -> None:
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

    def print_big(self, x, y, color, string):
        self.terminal.layer(110)
        self.terminal.color(color)
        self.terminal.print(x, y, f"[font=title]{string}[/font]")

    def draw_box(self, x, y, w, h, color, back: int = 0xFF151515):
        self.clear_area(x, y, w, h)
        self.fill_area(x-1, y-1, w, h, color=back, layer=99)
        self.terminal.layer(100)
        self.terminal.color(color)

        # upper border
        border = '┌' + '─' * (w - 2) + '┐'
        self.terminal.print(x - 1, y - 1, border)
        # sides
        for i in range(h - 2):
            # left
            self.terminal.print(x - 1, y + i, '│')
            # right
            self.terminal.print(x + (w - 2), y + i, '│')
        # lower border
        border = '└' + '─' * (w - 2) + '┘'
        self.terminal.print(x - 1, y + (h - 2), border)

    def draw_bar(self, x, y, w, value, maximum, fore):
        bar_width = round(w * 2 * (value / maximum))

        if bar_width == 0 and value > 1:
            bar_width = 1
        if bar_width == w * 2 and value < maximum:
            bar_width = w * 2 - 1

        for i in range(w):
            self.terminal.layer(99)
            self.terminal.clear_area(x + i, y, w, 1)
            self.terminal.color(0x88000000 + fore)
            self.terminal.print(x + i, y, "█")

        for i in range(w):
            char = " "
            if i < bar_width // 2:
                char = "█"
            elif i < (bar_width + 1) // 2:
                char = "▌"

            self.terminal.layer(100)
            self.terminal.color(0xFF000000 + fore)
            self.terminal.print(x + i, y, char)
