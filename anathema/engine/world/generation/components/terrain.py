from __future__ import annotations
from enum import Enum, auto

from ecstremity import Component
from anathema.engine.world.generation.tiles import Tiles


class TerrainTypes(Enum):
    UNFORMED = auto()
    FOREST = auto()
    DESERT = auto()
    PLAINS = auto()
    TUNDRA = auto()


class Map_Terrain(Component):

    def __init__(self) -> None:
        self._terrain_type: TerrainTypes = TerrainTypes.UNFORMED

    @property
    def terrain_type(self):
        return self._terrain_type

    @terrain_type.setter
    def terrain_type(self, value: TerrainTypes):
        self._terrain_type = value
