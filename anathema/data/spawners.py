from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING
from anathema.world.tile_factory import Depth


if TYPE_CHECKING:
    from anathema.world.area import Area
    from ecstremity import Engine, Entity


class ItemFactory:

    def __init__(self, area: Area, ecs: Engine) -> None:
        self.area = area
        self.ecs = ecs

    def spawn(self, definition: ItemType):
        item = self.ecs.create_entity()
        self.ecs.prefabs.apply_to_entity(
            item,
            definition.prefab,
            {'Position': {
                'x': definition.x,
                'y': definition.y,
                'z': Depth.ABOVE_1.value}})

@dataclass
class ItemType:
    name: str
    prefab: str
    x: int
    y: int


def spawner(name: str, prefab: str, x: int, y: int):
    return ItemType(name, prefab, x, y)


class Spawners:
    small_backpack = (lambda x, y : spawner('small_backpack', 'Small_Backpack', x, y))
