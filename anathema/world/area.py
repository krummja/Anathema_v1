from __future__ import annotations
from typing import *

from morphism import Size
from anathema.world.tile_factory import TileFactory
from anathema.world.tile_space import TileSpace
# from anathema.data.items.item_spawners import ItemFactory, ItemSpawners
# from anathema.core.options import Options

if TYPE_CHECKING:
    from anathema.world.region import Region


class Area:

    name: str = "<unset>"

    def __init__(
            self,
            region: Region,
            size: Size,
            tile_space: TileSpace = None,
        ) -> None:
        if not tile_space:
            tile_space = TileSpace(size)
        # self.items = ItemFactory(self, region.world.ecs)
        self.region = region
        self.size = size
        self.ecs = region.world.game.ecs.world
        self.factory = TileFactory(self, self.ecs, tile_space)
        self.initialize_area()

    def initialize_area(self) -> None:
        self.factory.build()
        # self.items.spawn(ItemSpawners.short_sword(9, 9))

    def get_entities_at(self, x: int, y: int):
        entities = self.ecs.entities
        result = []
        for entity in entities:
            if entity.has('Position'):
                if entity['Position'].xy == (x, y):
                    result.append(entity.uid)
        return result

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < int(self.size.width) and 0 <= y < int(self.size.height)):
            return True
        if not self.region.world.game.physics_system.passable[x][y]:
            return True
        return False

    def is_interactable(self, x: int, y: int) -> bool:
        if not (0 <= x < int(self.size.width) and 0 <= y < int(self.size.height)):
            return False
        if self.region.world.game.interaction_system.interactable[x][y]:
            return True
        return False
