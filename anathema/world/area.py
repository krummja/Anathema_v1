from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

import random
from anathema.world.tile_factory import TileFactory
from anathema.core.options import Options

if TYPE_CHECKING:
    from anathema.world.region import Region


class Area:

    def __init__(self, name: str, region: Region) -> None:
        self.factory = TileFactory(self, region.world.ecs)
        self.name = name
        self.region = region
        self.width = Options.STAGE_WIDTH
        self.height = Options.STAGE_HEIGHT
        self.factory.build()

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.region.world.game.physics_system.passable[x][y]:
            return True
        return False

    def is_interactable(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if self.region.world.game.interaction_system.interactable[x][y]:
            return True
        return False
