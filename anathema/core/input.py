from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Optional, Callable, TypeVar, Tuple

from anathema.abstracts import AbstractManager
from bearlibterminal import terminal as blt

if TYPE_CHECKING:
    from anathema.core import Game


T = TypeVar("T")


class CommandLibrary:

    COMMAND_KEYS: Dict[str, Dict[int, str]] = {
        'DEFAULT': {
            blt.TK_RETURN: "confirm",
            blt.TK_KP_ENTER: "confirm",
            blt.TK_ESCAPE: "escape",
            },
        'MAIN MENU': {
            blt.TK_ESCAPE: "escape",
            # blt.TK_Q: "quit",
            blt.TK_TAB: "next",
            blt.TK_RETURN: "confirm",
            },
        'STAGE': {
            blt.TK_D: "drop",
            blt.TK_E: "equipment",
            blt.TK_G: "pickup",
            blt.TK_I: "inventory",
            blt.TK_L: "examine",
            blt.TK_ESCAPE: "escape",
            }
        }

    MOVE_KEYS: Dict[int, Tuple[int, int]] = {
        # Arrow keys.
        blt.TK_LEFT: (-1, 0),
        blt.TK_RIGHT: (1, 0),
        blt.TK_UP: (0, -1),
        blt.TK_DOWN: (0, 1),
        blt.TK_HOME: (-1, -1),
        blt.TK_END: (-1, 1),
        blt.TK_PAGEUP: (1, -1),
        blt.TK_PAGEDOWN: (1, 1),
        blt.TK_PERIOD: (0, 0),
        # Numpad keys.
        blt.TK_KP_1: (-1, 1),
        blt.TK_KP_2: (0, 1),
        blt.TK_KP_3: (1, 1),
        blt.TK_KP_4: (-1, 0),
        blt.TK_KP_5: (0, 0),
        blt.TK_KP_6: (1, 0),
        blt.TK_KP_7: (-1, -1),
        blt.TK_KP_8: (0, -1),
        blt.TK_KP_9: (1, -1),
        }


class StateBreak(Exception):
    """Break the current state and force it to return None."""


class InputController(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._current_screen = game.screens.current_screen

    def handle_input(self) -> Optional[Callable[[], Optional[T]]]:
        key = self.game.renderer.terminal.read()
        try:
            command = self.command_lookup(key)
        except StateBreak:
            return None
        if command is not None:
            return command

    def command_lookup(self, key):
        if key in CommandLibrary.MOVE_KEYS:
            return self._current_screen.cmd_move(*CommandLibrary.MOVE_KEYS[key])
        try:
            if key in CommandLibrary.COMMAND_KEYS[self._current_screen.name]:
                commands = CommandLibrary.COMMAND_KEYS[self._current_screen.name]
                command = getattr(self._current_screen, f"cmd_{commands[key]}")
                return command
        except KeyError:
            if key in CommandLibrary.COMMAND_KEYS['DEFAULT']:
                commands = CommandLibrary.COMMAND_KEYS['DEFAULT']
                command = getattr(self._current_screen, f"cmd_{commands[key]}")
                return command
        else:
            return None
