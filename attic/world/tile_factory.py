from __future__ import annotations
from typing import *

import numpy as np

from anathema.world.tile_space import TileSpace
from anathema.world.depth import Depth
import cProfile
import pstats

if TYPE_CHECKING:
    from anathema.world.area import Area
    from ecstremity import World


def walk_array(array):
    for x in range(128):
        for y in range(128):
            definition = array[x, y]
            yield definition, x, y


class TileFactory:

    def __init__(self, area: Area, ecs: World, tile_space: TileSpace) -> None:
        self.area = area
        self.ecs = ecs
        self.tile_space = tile_space.initialize()

    def build(self):
        for definition, x, y in walk_array(self.tile_space):
            tile = self.ecs.create_entity()
            tile.add('Position', {'x': x, 'y': y, 'z': Depth.GROUND.value})
            tile.add('Renderable', {'char': definition.char, 'fore': definition.fore, 'back': definition.back})
            if definition.blocker:
                tile.add('Blocker', {})
            if definition.opaque:
                tile.add('IsOpaque', {})
            if definition.interactable:
                tile.add('IsInteractable', {})
