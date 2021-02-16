from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from enum import Enum

if TYPE_CHECKING:
    from ecstremity import Engine, Entity


class Depth(Enum):
    ABOVE_5 = 10
    ABOVE_4 = 9
    ABOVE_3 = 8
    ABOVE_2 = 7
    ABOVE_1 = 6
    GROUND  = 5
    BELOW_1 = 4
    BELOW_2 = 3
    BELOW_3 = 2
    BELOW_4 = 1

class TileFactory:

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs

    def build(
            self,
            x: int,
            y: int,
            z: Depth = Depth.GROUND,
            char: Optional[str] = None,
            fore: Optional[int] = None,
            blocker: Optional[bool] = None,
            opaque: Optional[bool] = None,
        ) -> Entity:
        tile = self.ecs.create_entity()
        if char is None:
            self.ecs.prefabs.apply_to_entity(
                tile,
                'unformed',
                {'Position': {'x': x, 'y': y, 'z': z}})
        else:
            if fore is None:
                fore = 0xFFFFFF
            tile.add('Position', {'x': x, 'y': y, 'z': 0})
            tile.add('Renderable', {'char': char, 'fore': fore})
            if blocker is not None:
                tile.add('Blocker', {})
            if opaque is not None:
                tile.add('Opaque', {})
        return tile.uid
