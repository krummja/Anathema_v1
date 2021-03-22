from __future__ import annotations
from typing import TYPE_CHECKING
from contextlib import contextmanager

from bearlibterminal import terminal
from morphism import Point, Rect

from anathema.core.options import Options
from anathema.core.terminal import BaseTerminal
from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class RenderManager(AbstractManager):
    """
    General purpose renderer for roguelike games.
    Access RenderManager.terminal to use the usual BearLibTerminal
    methods for drawing to screen, or directly access the methods on
    this class to access offset support and to use geometry classes
    for all positional parameters.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._terminal = BaseTerminal()
        self._crop_rect = None
        self._offset = Point(0, 0)
        self._fg = 0xFFFFFFFF
        self._bg = 0xFF151515

    @property
    def terminal(self) -> terminal:
        return self._terminal

    @property
    def color(self):
        return self._fg

    @property
    def bkcolor(self):
        return self._bg

    @color.setter
    def color(self, value):
        self._fg = value
        self._terminal.color(value)

    @bkcolor.setter
    def bkcolor(self, value):
        self._bg = value
        self._terminal.bkcolor(value)

    @contextmanager
    def translate(self, offset: Point):
        """Translate all positional renderer calls by the given `offset` by
        using the following syntax:

            offset = Point(x, y)  # let x = 2, y = 2
            with RenderManager.translate(offset):
                RenderManager.put(Point(0, 0), '@')  # puts at (2, 2)
        """
        previous = self._offset
        self._offset = self._offset + offset
        yield
        self._offset = previous

    def refresh(self) -> None:
        self._terminal.refresh()

    def setup(self) -> None:
        self._terminal.open()
        self._terminal.composition(True)
        self._terminal.bkcolor(self.bkcolor)

    def teardown(self) -> None:
        self._terminal.composition(False)
        self._terminal.close()

    def update(self) -> None:
        self.refresh()

    def clear(self) -> None:
        self._terminal.clear()
        self._terminal.bkcolor(self.bkcolor)

    def clear_area(self, rect: Rect, *args) -> None:
        computed_rect = Rect(rect.origin + self._offset, rect.size)
        if self._crop_rect and not self._crop_rect.intersects(computed_rect):
            return
        return self._terminal.clear_area(computed_rect, *args)

    def crop(self, rect: Rect, *args) -> None:
        computed_rect = Rect(rect.origin + self._offset, rect.size)
        if self._crop_rect and not self._crop_rect.intersects(computed_rect):
            return
        return self._terminal.crop(computed_rect, *args)

    def put(self, point, char):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.pick(computed_point, char)

    def print(self, point: Point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.puts(computed_point, *args)

    def print_big(self, point: Point, string: str):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        self.terminal.print(computed_point, f"[font=title]{string}[/font]")

    def pick(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.pick(computed_point, *args)

    def pick_color(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.pick_color(computed_point, *args)

    def pick_bkcolor(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.pick_bkcolor(computed_point, *args)

    def put_ext(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.put_ext(computed_point, *args)

    def read_str(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return self._terminal.read_str(computed_point, *args)

    def fill_area(self, rect: Rect, char: str = "█", layer: int = 0) -> None:
        self._terminal.layer(layer)
        self._terminal.color(self._bg)
        for _x in range(rect.left, rect.right):
            for _y in range(rect.top, rect.bottom):
                self._terminal.put(_x, _y, char)

    def fill(self, char: str = "█", color: int = 0xFF151515) -> None:
        self._terminal.layer(0)
        self._terminal.color(color)
        for x in range(Options.SCREEN_WIDTH):
            for y in range(Options.SCREEN_HEIGHT):
                self._terminal.put(x, y, char)

    def draw_box(self, rect: Rect, color):
        self.clear_area(rect)
        self.fill_area(rect, layer=99)
        self.terminal.layer(100)
        self.terminal.color(color)

        x = rect.left
        y = rect.top
        w = rect.width
        h = rect.height

        # upper border
        border = '┌' + '─' * (w - 2) + '┐'
        self.terminal.print(x, y, border)

        # sides
        for i in range(h - 2):
            # left
            self.terminal.print(x, y + 1 + i, '│')
            # right
            self.terminal.print(x + (w - 1), y + 1 + i, '│')

        # lower border
        border = '└' + '─' * (w - 2) + '┘'
        self.terminal.print(x, y + (h - 1), border)

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
