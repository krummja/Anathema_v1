from __future__ import annotations
from typing import *
import tcod

from .base_manager import BaseManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class InputManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def handle_input(self, key_events):
        for event in key_events:
            if self.game.screens.active_screen:
                self.game.screens.active_screen.dispatch(event)
                # handle input results

    def cmd_quit(self):
        pass
