from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class PlayerManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
