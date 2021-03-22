from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Callable
import weakref

from anathema.core.options import Options

from morphism import Point, Size
from anathema.screens.views.rectview import RectView

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class AbstractScreen:

    name: str

    def __init__(self, *args, **kwargs) -> None:
        self._manager: Callable[[], Optional[ScreenManager]] = lambda: None
        self.covers_screen: bool = True

    @property
    def manager(self):
        return self._manager()

    @manager.setter
    def manager(self, value):
        if value:
            self._manager = weakref.ref(value)
        else:
            self._manager = lambda: None

    # noinspection PyUnresolvedReferences
    @property
    def game(self) -> Game:
        if self._manager():
            return self._manager().game

    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass

    def become_active(self):
        pass

    def resign_active(self):
        pass

    def handle_input(self) -> None:
        command = self.game.input.handle_input()
        if not command:
            return
        command()

    def on_draw(self) -> None:
        pass

    def on_update(self, is_active=False):
        pass


class UIScreen(AbstractScreen):

    def __init__(self, views, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(views, list):
            views = [views]

        self.view = RectView(screen=self)

    def on_update(self, is_active=False):
        self.game.renderer.bkcolor = 0xFF151515
        self.view.frame = self.view.frame.with_size(
            Size(Options.SCREEN_WIDTH, Options.SCREEN_HEIGHT))
        self.view.perform_layout()
        self.view.perform_draw(self.manager.game.renderer)
        self.game.renderer.print(Point(1, 1), "Hello, world!")
