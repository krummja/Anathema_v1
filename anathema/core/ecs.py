from __future__ import annotations
from typing import TYPE_CHECKING

import os
import json
from ecstremity import EngineAdapter as Engine

from anathema.abstracts import AbstractManager
from anathema.components import all_components

if TYPE_CHECKING:
    from anathema.core.game import Game


JSON_PATH = "anathema/data/prefabs/"


class ECSManager(AbstractManager):
    """Manager class that wraps the `ecstremity` ECS Engine."""

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.engine = Engine(client=game)

        for component in all_components():
            self.engine.components.register(component)

        for file in self.load_prefab_files():
            file = JSON_PATH + file
            with open(file) as f:
                definition = json.load(f)
                self.engine.prefabs.register(definition)

    def load_prefab_files(self):
        return [f for f in os.listdir(JSON_PATH) if f.endswith('.json')]
