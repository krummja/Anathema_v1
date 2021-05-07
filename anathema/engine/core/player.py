from __future__ import annotations
from typing import *
from collections import deque

from ecstremity import EventData, Entity
from anathema.engine.core import BaseManager
from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class PlayerManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._uid = None
        self._action_queue = deque([])

    @property
    def entity(self):
        return self.game.ecs.world.get_entity(self._uid)

    @property
    def uid(self):
        return self._uid

    @property
    def position(self):
        return self.entity['Position'].xy

    def initialize(self):
        player = self.game.ecs.world.create_prefab("Player", {
            "position": {
                "area": self.game.world.current_area,
                "x": 10,
                "y": 20
            },
            "renderable": {
                "char": "@",
                "fg": (255, 0, 255)
            }
        }, uid="PLAYER")
        self._uid = player.uid

        test_npc: Entity = self.game.ecs.world.create_entity('test')
        test_npc.add("position", {"area": self.game.world.current_area, "x": 20, "y": 20})
        test_npc.add("renderable", {"char": "N", "fg": (0, 255, 255)})
        test_npc.add("actor", {})
        test_npc.add("legs", {})
        test_npc.add("brain", {})
        test_npc['Brain'].append_goal(BoredGoalType().create(self.game.ecs.world))
        test_npc.add("wandering", {})

    def get_next_action(self):
        try:
            return self._action_queue.popleft()
        except IndexError:
            pass

    def queue_action(self, action):
        self._action_queue.append(action)

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]
        self.queue_action((lambda: self.entity.fire_event(
            'try_move', EventData(target=(target_x, target_y)))))

    def wait(self, turns: int = 1):
        self.queue_action((lambda: self.entity.fire_event(
            'energy_consumed', EventData(cost=turns * 1000)
        )))
