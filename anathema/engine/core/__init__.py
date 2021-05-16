from __future__ import annotations
from typing import *
from anathema.utils.logging import log_init

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


@log_init
class BaseManager:

    def __init__(self, game: Game) -> None:
        self.game = game

    def __repr__(self):
        return repr(self.__class__.__name__)
