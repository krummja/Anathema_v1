from __future__ import annotations
from typing import TYPE_CHECKING
from anathema.world.tiles2D import Tiles2D, InitTiles

if TYPE_CHECKING:
    from ecstremity import Engine



class TileFactory:

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs

    def build(self, x: int, y: int):
        tile = self.ecs.create_entity()
        self.ecs.prefabs.apply_to_entity(tile, 'unformed', {'Position': {'x': x, 'y': y}})
        return tile


class TileMap(Tiles2D, InitTiles):

    def __init__(self, width: int, height: int, ecs) -> None:
        self.factory = TileFactory(ecs)
        super().__init__(width, height)

        self.entities = []
        self.entrances = []
        self.exits = []
