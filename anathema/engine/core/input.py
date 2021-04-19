from __future__ import annotations
from typing import *
import tcod

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class LoopExit(BaseException):
    """Break the loop, forcing the game to exit."""


T = TypeVar("T")


class InputManager(BaseManager, Generic[T], tcod.event.EventDispatch[T]):

    COMMAND_KEYS = {
        tcod.event.K_ESCAPE: 'escape',
        tcod.event.K_RETURN: 'return',
    }

    def __init__(self, game: Game):
        super().__init__(game)

    def update(self):
        all_input_events = list(tcod.event.get())
        key_events = [e for e in all_input_events if e.type == 'KEYDOWN']
        if len(key_events) > 0:
            event = key_events.pop()
            value = self.dispatch(event)
            if value is not None:
                return value

    def ev_keydown(self, event):
        func: Callable[[], T]
        if event.sym in self.COMMAND_KEYS:
            try:
                func = getattr(self.game.screens.active_screen, f"cmd_{self.COMMAND_KEYS[event.sym]}")
                return func()
            except AttributeError:
                self.game.screens.active_screen.handle_input(event)
