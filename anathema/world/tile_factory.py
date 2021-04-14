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
    for x in range(64):
        for y in range(64):
            definition = array[x, y]
            yield definition, x, y


class TileFactory:

    def __init__(self, area: Area, ecs: World, tile_space: TileSpace) -> None:
        self.area = area
        self.ecs = ecs
        self.tile_space = tile_space.initialize()

    def build(self):
        # profile = cProfile.Profile()
        # profile.enable()
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

        # for x in range(64):
        #     for y in range(64):
        #         tile_def = self.tile_space[x, y]
        #         tile = self.ecs.create_entity()
        #
        #         tile.add('Position', {'x': x, 'y': y, 'z': Depth.GROUND.value})
        #         tile.add('Renderable', {'char': tile_def.char, 'fore': tile_def.fore, 'back': tile_def.back})
        #         # tile.add('Noun', {'noun_text': tile_def.name})
        #
        #         if tile_def.blocker:
        #             tile.add('Blocker', {})
        #         if tile_def.opaque:
        #             tile.add('IsOpaque', {})
        #         if tile_def.interactable:
        #             tile.add('IsInteractable', {})
        #         # if tile_def._portal:
        #         #     if tile_def._is_closed:
        #         #         tile.add('Door', {})
        #         #     else:
        #         #         tile.add('Door', {})
        #         if tile_def.container:
        #             tile.add('Container', {'capacity': 10})
        # profile.disable()
        # ps1 = pstats.Stats(profile)
        # ps1.sort_stats('calls', 'cumtime')
        # ps1.print_stats(5)
        #
        # ps2 = pstats.Stats(profile)
        # ps2.sort_stats('tottime', 'cumtime')
        # ps2.print_stats(5)
