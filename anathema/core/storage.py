from __future__ import annotations
from typing import *

import os
import sys
import datetime
import traceback
import lzma
import pickle
import pickletools
from dataclasses import dataclass

from .base_manager import BaseManager

if TYPE_CHECKING:
    from anathema.core.player import PlayerManager
    from anathema.core.world import WorldManager


class SaveFile:

    def __init__(
            self,
            player_name: str,
            player_data,
            world_data
        ) -> None:
        self.player_name = player_name
        self.player_data = player_data
        self.world_data = world_data

    @property
    def save_file_name(self):
        return self.player_name + f"{datetime.datetime.now()}"


SAVE_PATH = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(SAVE_PATH, 'save.sav.xz')


class StorageManager(BaseManager):

    def __init__(self, game):
        super().__init__(game)
        self.save_time = datetime.datetime.now()
        self.saves = []

    def make_save(self):
        return SaveFile("Test", self.game.player, self.game.world)
