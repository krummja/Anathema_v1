from __future__ import annotations
from typing import *

from anathema.core import engine
from anathema.components import all_components
from .base_manager import BaseManager

if TYPE_CHECKING:
    from .game import Game


class ECSManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.engine = engine

        for component in all_components():
            self.engine.components.register(component)
