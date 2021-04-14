from __future__ import annotations
from typing import *
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from anathema.core.game import Game
    from ecstremity import Query, World


class BaseSystem(ABC):

    def __init__(self, game: Game) -> None:
        self.game = game
        self.ecs: World = game.ecs.world
        self._queries: Dict[str, Query] = {}
        self.initialize()

    def query(self, key: str, all_of=None, any_of=None, none_of=None):
        self._queries[key] = self.ecs.create_query(all_of, any_of, none_of)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self, dt) -> None:
        pass
