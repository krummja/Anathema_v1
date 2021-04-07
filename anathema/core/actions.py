from __future__ import annotations
from typing import *
from collections import deque

from .base_manager import BaseManager

if TYPE_CHECKING:
    from .game import Game


class ActionManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.action_queue = deque([])

    def get_next_action(self):
        return self.action_queue.popleft()

    def queue_action(self, action):
        self.action_queue.append(action)
