from __future__ import annotations
from typing import *
import tcod

from .base_manager import BaseManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class ConsoleManager(BaseManager):

    CONSOLE_WIDTH: int = 110
    CONSOLE_HEIGHT: int = 55

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.root_console = tcod.Console(self.CONSOLE_WIDTH, self.CONSOLE_HEIGHT)
