from __future__ import annotations
from typing import List, TYPE_CHECKING
from ecstremity.entity import Entity

from anathema.abstracts import AbstractSystem


if TYPE_CHECKING:
    from anathema.core.game import Game


class DestroySystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=[ 'IsDestroying' ])

    def update(self, dt) -> None:
        for entity in self._query.result:
            if entity['IsDestroying'].cycle > 0:
                entity.destroy()
                print("Destroyed entity")
            else:
                entity['IsDestroying'].cycle += 1
