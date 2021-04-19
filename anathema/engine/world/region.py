from __future__ import annotations
from typing import *

from .area import Area

if TYPE_CHECKING:
    from .world import World


class Region:

    name: str

    def __init__(self, world: World) -> None:
        self.world = world
        self.areas = {}

    def add_area(self, area: Area):
        self.areas[area.name] = area(self, 128, 128)
