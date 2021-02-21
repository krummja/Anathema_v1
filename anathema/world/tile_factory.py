from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from enum import Enum
from collections import defaultdict

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


class TileFactory(defaultdict):

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs

        self['unformed'] = (lambda x, y: self.build(x, y, char="?", blocker=True, opaque=True))
        self['unformed_wet'] = (lambda x, y : self.build(x, y, char="≈", fore=0xFF7492B5, wet=True))


    def build(
            self,
            x: int,
            y: int,
            z: Depth = Depth.GROUND,
            char: Optional[str] = "?",
            fore: Optional[int] = "0x00FFFFFF",
            blocker: Optional[bool] = False,
            opaque: Optional[bool] = False,
            wet: Optional[bool] = False,
            doorway: Optional[bool] = False,
        ) -> Entity:
        tile = self.ecs.create_entity()
        self.ecs.prefabs.apply_to_entity(
            tile,
            'unformed',
            {
                'Position': {
                    'x': x,
                    'y': y,
                    'z': z
                    },
                'Renderable': {
                    'char': char,
                    'fore': fore,
                    },
                'Unformed': {
                    'blocker': blocker,
                    'opaque': opaque,
                    'wet': wet,
                    'doorway': doorway,
                    }
                })

        if tile.has('Unformed'):
            if tile['Unformed'].blocker:
                tile.add('Blocker', {})
            if tile['Unformed'].opaque:
                tile.add('Opaque', {})

        return tile.uid
