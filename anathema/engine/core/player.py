from __future__ import annotations
from typing import *
from collections import deque

from ecstremity import EventData
from anathema.engine.core import BaseManager

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
                "x": 10, "y": 20
            },
            "renderable": {
                "char": "@",
                "fg": (255, 0, 255)
            }
        })
        self._uid = player.uid

    def get_next_action(self):
        return self._action_queue.popleft()

    def queue_action(self, action):
        self._action_queue.append(action)

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]
        self.queue_action((lambda: self.entity.fire_event(
            'try_move', EventData(target=(target_x, target_y)))))
