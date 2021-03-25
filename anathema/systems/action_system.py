from __future__ import annotations
from typing import TYPE_CHECKING
from collections import deque

from anathema.systems.system import AbstractSystem

if TYPE_CHECKING:
    from anathema.core import Game


class ActionSystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._query = self.ecs.create_query(
            all_of=[ 'Actor' ])

    def update(self, dt) -> bool:
        entities = self._query.result
        entities = deque(sorted(entities, key=lambda e: e['Actor']))

        entity = entities.popleft()

        if entity and not entity['Actor'].has_energy:
            self.game.clock.increment(-1 * entity['Actor'].energy)
            for entity in entities:
                entity['Actor'].add_energy(self.game.clock.tick_delta)

        while entity and entity['Actor'].has_energy:
            if entity.has('IsPlayer'):
                try:
                    action = self.game.player.get_next_action()
                    if action:
                        action.act()
                        return True
                    continue
                except IndexError:
                    return False

            entity.fire_event('take_action')
            entity = entities.popleft()

        return False
