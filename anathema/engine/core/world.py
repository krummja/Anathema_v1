from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class WorldManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._current_area = None

    @property
    def current_area(self):
        return self._current_area
