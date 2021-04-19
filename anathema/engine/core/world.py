from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager
from anathema.engine.world.world import World

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class WorldManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._world = None

    def initialize_world(self):
        self._world = World(self.game)
