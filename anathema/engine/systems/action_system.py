from __future__ import annotations
from typing import *
from collections import deque
import logging

from anathema.engine.systems import BaseSystem

from anathema.engine.data.skills import SKILL_SPEED, get_skill_value

if TYPE_CHECKING:
    pass


ACTION_COST = 100
GAINS = [15, 20, 24, 30, 40, 50, 60, 80, 100, 120, 150, 180, 240]


class ActionSystem(BaseSystem):

    def initialize(self):
        self.query('actors', all_of=[ 'Actor' ])

    # def update(self):
    #     entities = self._queries['actors'].result
    #     sorted_entities = deque(sorted(entities, key=(lambda e: e['Actor']), reverse = True))
    #     entity = sorted_entities[0]
    #
    #     if entity and not entity['Actor'].can_take_turn:
    #         entity['Actor'].add_energy(GAINS[get_skill_value(SKILL_SPEED, entity)])

    def update(self):
        entities = self._queries['actors'].result
        # self.game.maps.current_area.actors.update(set(entities))
        self.game.maps.actors.update(set(entities))

        sorted_entities = deque(sorted(entities, key=(lambda e: e['Actor']), reverse = True))
        entity = sorted_entities[0]

        if entity and not entity['Actor'].has_energy:
            self.game.clock.increment(-1 * entity['Actor'].energy)
            for entity in entities:
                entity['Actor'].add_energy(1000)

        while entity and entity['Actor'].has_energy:
            if entity.has('IsPlayer'):
                action = self.game.player.get_next_action()
                if action:
                    action()
                return True

            entity.fire_event('take_action')
            if len(entities) > 0:
                entity = sorted_entities.popleft()

        return False
