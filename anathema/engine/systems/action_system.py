from __future__ import annotations
from typing import *
from collections import deque

from anathema.engine.systems import BaseSystem

if TYPE_CHECKING:
    pass


class ActionSystem(BaseSystem):

    def initialize(self):
        self.query('actors', all_of=[ 'Actor' ])

    def update(self):
        entities = self._queries['actors'].result
        entities = deque(sorted(entities, key=(lambda e: e['Actor'])))
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
                        action()
                    return True
                except IndexError:
                    return False
            entity.fire_event('take_action')
            entity = entities.popleft()
        return False
