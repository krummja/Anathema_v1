from __future__ import annotations
from typing import *
from morphism import *
import tcod

from anathema.engine.core.options import Options
from anathema.interface.views.first_responder import FirstResponderView

if TYPE_CHECKING:
    from anathema.interface.views import View
    from anathema.engine.core.game import Game


T = TypeVar("T")


class BaseScreen:

    def __init__(self, name: str, game: Game) -> None:
        self.name = name
        self.game = game

        self._input_handlers = []
        self.covers_screen: bool = True

    def add_input_handler(self, handler):
        if not getattr(handler, 'handle_input'):
            raise ValueError("Invalid handler")
        self._input_handlers.append(handler)

    def remove_input_handler(self, handler):
        self._input_handlers.remove(handler)

    def handle_input(self, event):
        for handler in self._input_handlers:
            handler.handle_input(event)

    def on_update(self, is_active=False) -> bool:
        return True


class Screen(BaseScreen):

    def __init__(self, name: str, game: Game) -> None:
        super().__init__(name, game)

    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass

    def become_active(self):
        pass

    def resign_active(self):
        pass


class UIScreen(Screen):

    def __init__(self, name: str, game: Game, views: List[View]) -> None:
        super().__init__(name, game)
        if not isinstance(views, list):
            views = [views]
        self.view = FirstResponderView(subviews=views, screen=self)
        self.add_input_handler(self.view)

    def on_update(self, is_active=False):
        self.game.console.root.clear()
        self.view.frame = self.view.frame.with_size(
            Size(Options.CONSOLE_WIDTH, Options.CONSOLE_HEIGHT))
        self.view.perform_layout()
        self.view.perform_draw()
        return True
