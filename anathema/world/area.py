from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.world.tilemap import TileMap

if TYPE_CHECKING:
    from anathema.world.region import Region


class Area:

    def __init__(self, name: str, region: Region) -> None:
        self.name = name
        self.region = region
        self.tiles = TileMap(64, 64, self.region.world.ecs)
        self.width = 64
        self.height = 64

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 1 <= y < self.height):
            return True
        if not self.region.world.game.physics_system.passable[x][y]:
            return True
        return False
