from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class BaseManager:

    def __init__(self, game: Game) -> None:
        self.game = game
