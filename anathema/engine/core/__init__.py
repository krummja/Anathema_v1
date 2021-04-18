from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    pass


class BaseGame:
    """Base class for the core game engine."""


class BaseManager:

    def __init__(self, game: BaseGame) -> None:
        self.game = game
