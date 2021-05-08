from __future__ import annotations
from typing import *

from anathema.engine.world.tilemap import TileMap
from anathema.engine.world.generation.array_tools import rng_selection

if TYPE_CHECKING:
    pass


class AreaGenerator:

    @staticmethod
    def generate(settings: Dict[str, Any]) -> TileMap:
        return TileMap(settings["width"], settings["height"])

    @staticmethod
    def populate(tile_map: TileMap, settings: Dict[str, Any]):
        tile_map.tiles[:] = tile_map._tile_registry.unformed.make()
