from __future__ import annotations
from typing import *

from dataclasses import dataclass
import copy
import os
import sys
import time
import datetime
import lzma
import pickle
import pickletools
import sys
import traceback

if TYPE_CHECKING:
    from anathema.engine.world.tilemap import TileMap
    from anathema.engine.core.world import WorldData, AreaData
    from ecstremity import Component


ROOT_DIR = os.path.dirname(__file__)


def get_data(path: str) -> str:
    ASSET_DIR = os.path.join(ROOT_DIR, "_assets")
    assert os.path.exists(ASSET_DIR), f"Cannot find asset path: {ASSET_DIR}"
    return os.path.join(ASSET_DIR, path)


def get_save(path: str) -> str:
    SAVE_DIR = os.path.join(ROOT_DIR, "_saves")
    assert os.path.exists(SAVE_DIR), f"Cannot find save path: {SAVE_DIR}"
    return os.path.join(SAVE_DIR, path)


class CharacterRegistry:

    def __init__(self):
        self.index = 0
        self.data = {}

    def add(self, data):
        self.data[self.index] = data
        self.index += 1

    def load(self, index):
        return self.data[index]


@dataclass
class CharacterSave:
    name: str
    level: int
    area: str
    uid: str
    components: List[Component]


@dataclass
class WorldSave:
    world_id: str
    buildable: np.ndarray
    area_registry: Dict[Tuple[int, int], AreaData]


class GameData:

    def __init__(self):
        self._character: Optional[CharacterSave] = None
        self._world: Optional[WorldSave] = None

    def add_character(self, character: CharacterSave) -> None:
        self._character = character

    def load_character(self) -> CharacterSave:
        return self._character

    def add_world(self, world: WorldSave) -> None:
        self._world = world

    def load_world(self) -> WorldSave:
        return self._world


class Storage:

    @staticmethod
    def add_character(game_data: GameData, character: CharacterSave) -> None:
        game_data.add_character(character)

    @staticmethod
    def load_character(game_data: GameData) -> CharacterSave:
        return game_data.load_character()

    @staticmethod
    def add_world(game_data: GameData, world: WorldSave) -> None:
        for area in world.area_registry.values():
            area.tile_map.actors = None
        game_data.add_world(world)

    @staticmethod
    def load_world(game_data: GameData) -> WorldSave:
        return game_data.load_world()

    @staticmethod
    def write_to_file(data: GameData, file: str) -> None:
        data = pickle.dumps(data, protocol=4)
        with open(get_save(file), "wb") as f:
            f.write(data)

    @staticmethod
    def load_from_file(file: str) -> GameData:
        try:
            with open(get_save(file), "rb") as f:
                data = pickle.loads(f.read())
                return data
        except Exception:
            traceback.print_exc(file=sys.stderr)
