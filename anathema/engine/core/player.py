from __future__ import annotations
from typing import *
from collections import deque
import logging

from anathema.engine.core import BaseManager
from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType

if TYPE_CHECKING:
    from ecstremity import Entity
    from anathema.engine.core.game import Game
    from anathema.engine.core.session import Session


class PlayerManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._uid = None
        self._action_queue = deque([])

    @property
    def entity(self) -> Entity:
        return self.game.ecs.world.get_entity(self._uid)

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @property
    def position(self) -> Tuple[int, int]:
        return self.entity['Position'].xy

    def initialize(self) -> None:
        player = self.game.ecs.world.create_prefab("Player", {
            "position": {
                "area": self.game.world.current_area,
                "x": 247,
                "y": 247
            },
            "renderable": {
                "char": "@",
                "fg": (255, 255, 255)
            },
            "moniker": {
                "name": "Aulia Inuicta"
            }
        })
        self._uid = player.uid

    def teardown(self):
        self.game.ecs.world.destroy_entity(self.uid)

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
            'try_move', {"target": (target_x, target_y)})))

    def wait(self, turns: int = 1) -> None:
        self.queue_action((lambda: self.entity.fire_event(
            'energy_consumed', {"cost": turns * 1000}
        )))
