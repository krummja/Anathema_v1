from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.world.area import Area

if TYPE_CHECKING:
    from anathema.core.world import WorldManager



class Region:

    def __init__(self, name: str, world: WorldManager) -> None:
        self.name = name
        self.world = world
        self.areas = {}

    def add_area(self, name: str):
        self.areas[name] = Area(name, self)
