from __future__ import annotations
from typing import *
from morphism import *
from tcod import Console
from contextlib import contextmanager

from anathema.engine.core import BaseManager
from anathema.engine.core.options import Options

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class Context:

    def __init__(self, console: Console) -> None:
        self._offset = Point(0, 0)
        self.console = console

    def set_fg(self, rect: Rect, value):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.fg[
            computed.y:computed.y + computed.height,
            computed.x:computed.x + computed.width
        ] = value

    def set_bg(self, rect: Rect, value):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.bg[
            computed.y:computed.y + computed.height,
            computed.x:computed.x + computed.width
        ] = value

    @contextmanager
    def translate(self, offset: Point):
        previous = self._offset
        self._offset = self._offset + offset
        yield
        self._offset = previous

    def blit(self):
        pass

    def clear_area(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.draw_rect(
            computed,
            ch=32,
            fg=self.console.default_fg,
            bg=self.console.default_bg,
            *args, **kwargs
        )

    def draw_frame(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.draw_frame(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def draw_rect(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.draw_rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def get_height_rect(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.get_height_rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def hline(self, point: Point, *args, **kwargs):
        computed = point + self._offset
        self.console.hline(int(computed.x), int(computed.y), *args, **kwargs)

    def print(self, point: Point, *args, **kwargs):
        computed = point + self._offset
        self.console.print(int(computed.x), int(computed.y), *args, **kwargs)

    def print_(self, point: Point, *args, **kwargs):
        computed = point + self._offset
        self.console.print_(int(computed.x), int(computed.y), *args, **kwargs)

    def print_box(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.print_box(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def print_frame(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.print_frame(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def print_rect(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.print_rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def put_char(self, point: Point, *args, **kwargs):
        computed = point + self._offset
        self.console.put_char(int(computed.x), int(computed.y), *args, **kwargs)

    def rect(self, rect: Rect, *args, **kwargs):
        computed = Rect(rect.origin + self._offset, rect.size)
        self.console.rect(
            computed.x,
            computed.y,
            computed.width,
            computed.height,
            *args, **kwargs
        )

    def vline(self, point: Point, *args, **kwargs):
        computed = point + self._offset
        self.console.vline(int(computed.x), int(computed.y), *args, **kwargs)


class ConsoleManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.root = Console(Options.CONSOLE_WIDTH, Options.CONSOLE_HEIGHT)
        self.root.default_bg = (21, 21, 21)
        self.context = Context(self.root)
