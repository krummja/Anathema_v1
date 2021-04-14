from __future__ import annotations
from typing import *

from ecstremity import Engine
from anathema.components import all_components
from .base_manager import BaseManager

if TYPE_CHECKING:
    from .game import Game


class ECSManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.engine = Engine(client=game)
        self.world = self.engine.create_world()

    def initialize(self):
        for component in all_components():
            self.engine.register_component(component)
