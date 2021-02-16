from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from anathema.core.game import Game
    from ecstremity import Query, Engine


class AbstractSystem(ABC):

    def __init__(self, game: Game) -> None:
        self.game = game
        self.ecs: Engine = game.ecs.engine
        self._query: Optional[Query] = None

    @abstractmethod
    def update(self) -> None:
        pass
