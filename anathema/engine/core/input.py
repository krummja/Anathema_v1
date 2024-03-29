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
        tcod.event.K_c: 'character_info',
        tcod.event.K_F1: 'debug_f1',
        tcod.event.K_F2: 'spawn'
    }

    MOVE_KEYS: Dict[int, Tuple[int, int]] = {
        # Arrow keys.
        tcod.event.K_LEFT    : (-1, 0),
        tcod.event.K_RIGHT   : (1, 0),
        tcod.event.K_UP      : (0, -1),
        tcod.event.K_DOWN    : (0, 1),
        tcod.event.K_HOME    : (-1, -1),
        tcod.event.K_END     : (-1, 1),
        tcod.event.K_PAGEUP  : (1, -1),
        tcod.event.K_PAGEDOWN: (1, 1),
        # Numpad keys.
        tcod.event.K_KP_1    : (-1, 1),
        tcod.event.K_KP_2    : (0, 1),
        tcod.event.K_KP_3    : (1, 1),
        tcod.event.K_KP_4    : (-1, 0),
        tcod.event.K_KP_6    : (1, 0),
        tcod.event.K_KP_7    : (-1, -1),
        tcod.event.K_KP_8    : (0, -1),
        tcod.event.K_KP_9    : (1, -1),
    }

    def __init__(self, game: Game):
        super().__init__(game)

    def update(self):
        for event in tcod.event.get():
            value = self.dispatch(event)
            if value is not None:
                return value

    def ev_textinput(self, event):
        self.game.screens.active_screen.handle_textinput(event)

    def ev_keydown(self, event):
        self.game.screens.active_screen.handle_input(event)

        func: T
        if event.sym in self.COMMAND_KEYS:
            try:
                func = getattr(self.game.screens.active_screen, f"cmd_{self.COMMAND_KEYS[event.sym]}")
                return func()
            except AttributeError:
                pass

        if self.game.screens.active_screen:
            if self.game.screens.active_screen.name == 'STAGE':
                if event.sym in self.MOVE_KEYS:
                    self.game.player.move(self.MOVE_KEYS[event.sym])

                if event.sym == tcod.event.K_KP_5:
                    self.game.player.wait()
