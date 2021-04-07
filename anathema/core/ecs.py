from __future__ import annotations
from typing import *

from .base_manager import BaseManager

if TYPE_CHECKING:
    from .game import Game


class ECSManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
