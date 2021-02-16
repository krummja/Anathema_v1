from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from anathema.world.tiles2D import Tiles2D, InitTiles

if TYPE_CHECKING:
    from ecstremity import Engine, Entity


class TileFactory:

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs

    def build(
            self,
            x: int,
            y: int,
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
                {'Position': {'x': x, 'y': y}})
        else:
            if fore is None:
                fore = 0xFFFFFFFF
            tile.add('Position', {'x': x, 'y': y})
            tile.add('Renderable', {'char': char, 'fore': fore})
            if blocker is not None:
                tile.add('Blocker', {})
            if opaque is not None:
                tile.add('Opaque', {})

        return tile


class TileMap(Tiles2D, InitTiles):

    def __init__(self, width: int, height: int, ecs) -> None:
        self.factory = TileFactory(ecs)
        super().__init__(width, height)

        self.entities = []
        self.entrances = []
        self.exits = []
