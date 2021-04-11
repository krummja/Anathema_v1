from __future__ import annotations
from typing import *

from .base_manager import BaseManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class UIManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.screen = game.active_screen
        self.queue = []
        self.subscribers = {}

    def notify(self, data):
        pass

    def subscribe(self, subscriber):
        pass

    def unsubscribe(self, subscriber):
        pass

    def update(self):
        for option in self.queue:
            pass
