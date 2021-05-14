from __future__ import annotations
from typing import *

from dataclasses import dataclass
import copy
import os
import json
import sys
import time
import datetime
import lzma
import pickle
import pickletools
import sys
import traceback

if TYPE_CHECKING:
    from ecstremity import Component, Entity
    from anathema.engine.core.world import AreaData


ROOT_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(ROOT_DIR, "_assets")
SAVE_DIR = os.path.join(ROOT_DIR, "_saves")
CONTENT_DIR = os.path.join(ROOT_DIR, "content")


@dataclass
class CharacterSave:
    name: str
    uid: str
    world_id: str


@dataclass
class WorldSave:
    world_id: str
    buildable: np.ndarray
    area_registry: Dict[Tuple[int, int], AreaData]


class GameData:

    def __init__(
            self,
            save_id: str,
            world_save: WorldSave
        ) -> None:
        self.save_id = save_id
        self._world_save = world_save
        self._character_save: Optional[CharacterSave] = None
        self._queries = None

    @property
    def world_save(self) -> WorldSave:
        return self._world_save

    @world_save.setter
    def world_save(self, value) -> None:
        self._world_save = value

    @property
    def character_save(self) -> CharacterSave:
        return self._character_save

    @character_save.setter
    def character_save(self, value: CharacterSave) -> None:
        self._character_save = value

    @property
    def queries(self):
        return self._queries

    @queries.setter
    def queries(self, value):
        self._queries = value
