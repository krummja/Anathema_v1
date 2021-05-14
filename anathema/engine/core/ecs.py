from __future__ import annotations
from typing import *

from ecstremity import Engine
from anathema.engine.components import game_object_components
from anathema.engine.world.components import world_object_components
from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from ecstremity import World
    from anathema.engine.core.game import Game


class ECSManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.engine = Engine(client=game)
        self.world: Optional[World] = None

    def new_world(self):
        if not self.world:
            self.world = self.engine.create_world()
            self._register_components()
        else:
            raise AttributeError("Already existing world! Delete the current world first.")

    def delete_world(self):
        self.engine.destroy_world(self.world)
        self.world = None

    def serialize(self):
        return self.world.serialize()

    def _register_components(self):
        for component in game_object_components():
            self.engine.register_component(component)
        for component in world_object_components():
            self.engine.register_component(component)
