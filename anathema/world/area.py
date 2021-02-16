from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.world.tilemap import TileMap

if TYPE_CHECKING:
    from anathema.world.region import Region


class Area:

    def __init__(self, name: str, region: Region) -> None:
        self.name = name
        self.region = region
        self.width = 64
        self.height = 64
        self.tiles = TileMap(self.width, self.height, self.region.world.ecs)

        for x in range(10, 30):
            self.tiles.tiles[x][10].add('Blocker', {})
            self.tiles.tiles[x][10].add('Opaque', {})


    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.region.world.game.physics_system.passable[x][y]:
            return True
        return False
