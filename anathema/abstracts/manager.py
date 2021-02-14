from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from anathema.core.game import Game


class AbstractManager(ABC):

    def __init__(self, game: Game) -> None:
        self.game = game
