from __future__ import annotations
from typing import *
from tcod import Console

from anathema.engine.core import BaseManager
from anathema.engine.core.options import Options

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class ConsoleManager(BaseManager):

    def __init__(self, game: BaseGame):
        super().__init__(game)
        self.root = Console(Options.CONSOLE_WIDTH, Options.CONSOLE_HEIGHT)
