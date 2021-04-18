from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

from anathema.interface import *

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class ScreenManager(BaseManager):

    def __init__(self, game: BaseGame):
        super().__init__(game)
        self.screens = {
            'MAIN MENU': MainMenu(game),
        }
