from __future__ import annotations
from typing import *
from morphism import *
import tcod

from anathema.screens.views.first_responder import FirstResponderContainerView


T = TypeVar("T")


class BaseScreen(Generic[T], tcod.event.EventDispatch[T]):

    name: str

    def __init__(self):
        self._manager = None
        self._input_handlers = []
        self.covers_screen: bool = True

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, value):
        self._manager = value

    def add_input_handler(self, handler):
        if not getattr(handler, 'handle_input'):
            raise ValueError("Invalid handler")
        self._input_handlers.append(handler)

    def remove_input_handler(self, handler):
        self._input_handlers.remove(handler)

    def ev_keydown(self, event: tcod.event.KeyDown):
        self.handle_input(event)
        for handler in self._input_handlers:
            handler.handle_input(event)
        return True

    def handle_input(self, event):
        pass

    def on_update(self, is_active=False):
        return True


class Screen(BaseScreen):

    def __init__(self):
        super().__init__()

    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass

    def become_active(self):
        pass

    def resign_active(self):
        pass


class UIScreen(Screen):

    def __init__(self, views):
        super().__init__()
        if not isinstance(views, list):
            views = [views]
        self.view = FirstResponderContainerView(subviews=views, screen=self)
        self.add_input_handler(self.view)

    def on_update(self, is_active=False):
        self.view.frame = self.view.frame.with_size(
            Size(self.manager.game.console.CONSOLE_WIDTH, self.manager.game.console.CONSOLE_HEIGHT))
        self.view.perform_layout()
        self.view.perform_draw(self.manager.game.console.root_console)
        return True
