from __future__ import annotations
from typing import *
import os
import json

from anathema.engine.core import BaseManager
from anathema.data import DATA_DIR

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class ContentManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)

    def load_game_object_prefabs(self):
        path = os.path.join(DATA_DIR, "game_object_prefabs/")
        prefabs = [f for f in os.listdir(path) if f.endswith(".json")]
        for prefab in prefabs:
            with open(path + prefab) as f:
                definition = json.load(f)
                self.game.ecs.engine.prefabs.register(definition)

    def load_world_prefabs(self):
        path = os.path.join(DATA_DIR, "world_prefabs/")
        prefabs = [f for f in os.listdir(path) if f.endswith(".json")]
        for prefab in prefabs:
            with open(path + prefab) as f:
                definition = json.load(f)
                self.game.ecs.engine.prefabs.register(definition)

    def unload_prefabs(self):
        self.game.ecs.engine.prefabs.clear()
