from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class RenderManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.root_console = self.game.console.root
