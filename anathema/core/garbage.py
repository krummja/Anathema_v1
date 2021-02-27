from __future__ import annotations

from typing import TYPE_CHECKING

from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class GarbageCollection(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.queue = []

    def destroy(self):
        for entity in self.queue:
            self.game.ecs.engine.entities.destroy(entity.uid)
        self.queue.clear()

    def schedule(self, entity):
        self.queue.append(entity)

    def update(self, dt):
        self.destroy()
