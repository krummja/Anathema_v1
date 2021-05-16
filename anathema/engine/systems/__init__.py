from __future__ import annotations
from typing import *
from anathema.utils.logging import log_init

if TYPE_CHECKING:
    from anathema.engine.core.game import Game
    from ecstremity import Query, World


@log_init
class BaseSystem:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.ecs = game.ecs
        self._queries: Dict[str, Query] = {}
        self.initialize()

    def query(self, key: str, all_of=None, any_of=None, none_of=None) -> None:
        self._queries[key] = self.ecs.world.create_query(all_of, any_of, none_of)

    def initialize(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
