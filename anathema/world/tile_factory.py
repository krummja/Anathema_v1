from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from anathema.world.tile_space import TileSpace
from anathema.world.depth import Depth

if TYPE_CHECKING:
    from anathema.world.area import Area
    from ecstremity import Engine, Entity


class TileFactory:

    def __init__(self, area: Area, ecs: Engine) -> None:
        self.area = area
        self.ecs = ecs
        self.tile_space = TileSpace.initialize()

    def build(self):
        for x in range(self.area.width):
            for y in range(self.area.height):
                tile_def = self.tile_space[x, y]
                tile = self.ecs.create_entity()

                tile.add('Position', {'x': x, 'y': y, 'z': Depth.GROUND.value})
                tile.add('Renderable', {'char': tile_def.char, 'fore': tile_def.fore, 'back': tile_def.back})
                tile.add('Name', {'noun_text': tile_def.name})

                if tile_def._blocker:
                    tile.add('Blocker', {})
                if tile_def._opaque:
                    tile.add('Opacity', {})
                if tile_def._interactable:
                    tile.add('IsInteractable', {})
                if tile_def._portal:
                    if tile_def._is_closed:
                        tile.add('Door', {})
                    else:
                        tile.add('Door', {})
                if tile_def._container:
                    tile.add('Container', {'capacity': 10})
