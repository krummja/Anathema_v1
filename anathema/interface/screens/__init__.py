from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class BaseScreen:

    def __init__(self, name: str, game: BaseGame) -> None:
        self.name = name
        self.game = game
