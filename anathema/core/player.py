from __future__ import annotations
from collections import deque
from typing import *
from ecstremity import EventData

from .base_manager import BaseManager

if TYPE_CHECKING:
    from ecstremity import Entity
    from .game import Game


class PlayerManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._uid = None
        self._action_queue = deque([])
        self.ecs = self.game.ecs.world

    @property
    def entity(self) -> Entity:
        return self.ecs.get_entity(self._uid)

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def is_turn(self) -> bool:
        return self.entity['Actor'].has_energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.entity['Position'].xy

    def initialize(self):
        player = self.ecs.create_entity()
        player.add('IsPlayer', {})
        player.add('Position', {'x': 10, 'y': 10, 'z': 6})
        player.add('Renderable', {'char': '@', 'fore': "0xFFFF00FF"})
        player.add('Actor', {})
        player.add('Brain', {})
        player.add('Eyes', {})
        player.add('Legs', {})
        self._uid = player.uid

    def get_next_action(self):
        return self._action_queue.popleft()

    def queue_action(self, action):
        self._action_queue.append(action)

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]

        self.queue_action((lambda: self.entity.fire_event(
            'try_move',
            EventData(target=(target_x, target_y)))))
