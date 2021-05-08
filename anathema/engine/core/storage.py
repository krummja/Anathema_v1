from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class StorageManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.characters = {
            0: {
                "name": "Aulia Inuicta",
                "level": 1,
                "location": "Test Area"
            }
        }
        self._active_character = self.characters[0]

    @property
    def active_character(self):
        return self._active_character

    def new_character(self):
        pass

    def load_character(self):
        pass

    def delete_character(self):
        pass

    def save_character(self):
        pass
