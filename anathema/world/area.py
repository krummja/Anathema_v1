from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from anathema.world.tilemap import TileFactory, Depth
from anathema.core.options import Options

if TYPE_CHECKING:
    from anathema.world.region import Region


class Area:

    def __init__(self, name: str, region: Region) -> None:
        self.factory = TileFactory(region.world.ecs)
        self.name = name
        self.region = region
        self.width = Options.STAGE_WIDTH
        self.height = Options.STAGE_HEIGHT
        self.tiles = np.zeros((64, 64, 11), dtype=object, order="F")

    def fill(self):
        for x in range(Options.STAGE_WIDTH):
            for y in range(Options.STAGE_HEIGHT):
                z = Depth.GROUND.value
                self.tiles[x, y, z] = self.factory.build(x, y, Depth.GROUND)

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.region.world.game.physics_system.passable[x][y]:
            return True
        return False
