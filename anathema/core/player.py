from __future__ import annotations
from collections import deque
from typing import *

from .base_manager import BaseManager

if TYPE_CHECKING:
    from ecstremity import Entity
    from .game import Game


class PlayerManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._uid = None
        self._action_queue = deque([])
        self.initialize()

    @property
    def entity(self) -> Entity:
        return self.game.ecs.engine.get_entity(self._uid)

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
        player = self.game.ecs.engine.create_entity()
        player.add('Position', {'x': 10, 'y': 10})
        player.add('Renderable', {'char': '@', 'fore': "0xFFFF00FF"})
        player.add('Actor', {})
        print(player.components)
        self._uid = player.uid

    def get_next_action(self):
        return self._action_queue.popleft()

    def queue_action(self, action):
        self._action_queue.append(action)
