from __future__ import annotations
from typing import *

from morphism import Size
from anathema.world.area import Area

if TYPE_CHECKING:
    from anathema.core.world import WorldManager


class Region:

    def __init__(self, name: str, world: WorldManager) -> None:
        self.name = name
        self.world = world
        self.areas = {}

    def add_area(self, area: Type[Area], size: Size = Size(64, 64), tile_factory = None):
        if tile_factory:
            self.areas[area.name] = area(self, size, tile_factory)
        else:
            self.areas[area.name] = area(self, size)
