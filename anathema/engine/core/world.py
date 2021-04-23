from __future__ import annotations
from typing import *

import tcod.map

from anathema.engine.core import BaseManager
from anathema.engine.world.area import Area
from anathema.engine.world.tile import Tile

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


TILE = Tile('test', 1, True, ord("#"), (150, 150, 150), (21, 21, 21))


class TestArea(Area):

    name: str = "Test"

    def __init__(self):
        super().__init__(128, 128)

    def initialize(self):
        self._tiles[:] = TILE


class WorldManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.current_area = None

    def initialize(self):
        self.current_area = TestArea()
        self.current_area.initialize()
