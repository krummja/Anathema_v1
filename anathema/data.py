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
    from anathema.engine.world.tilemap import TileMap
    from anathema.engine.core.world import WorldData, AreaData
    from ecstremity import Component


ROOT_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(ROOT_DIR, "_assets")
SAVE_DIR = os.path.join(ROOT_DIR, "_saves")
CONTENT_DIR = os.path.join(ROOT_DIR, "content")


def get_data(path: str) -> str:
    assert os.path.exists(ASSET_DIR), f"Cannot find asset path: {ASSET_DIR}"
    return os.path.join(ASSET_DIR, path)


def get_save(path: str) -> str:
    assert os.path.exists(SAVE_DIR), f"Cannot find save path: {SAVE_DIR}"
    return os.path.join(SAVE_DIR, path)


class Manifest:
    data = {"saves": {}}

    @staticmethod
    def load():
        if not os.path.exists(os.path.join(SAVE_DIR, "manifest.json")):
            with open(os.path.join(SAVE_DIR, "manifest.json"), "w") as manifest:
                json.dump(Manifest.data, manifest)
        with open(os.path.join(SAVE_DIR, "manifest.json"), "r") as manifest:
            Manifest.data = json.load(manifest)

    @staticmethod
    def save():
        with open(os.path.join(SAVE_DIR, "manifest.json"), "w") as manifest:
            json.dump(Manifest.data, manifest)

    @staticmethod
    def update(data: GameData):
        Manifest.data["saves"].update({data.save_id: data.save_id + ".sav"})
        Manifest.save()


@dataclass
class CharacterSave:
    name: str
    level: int
    uid: str
    world_id: str
    components: Dict[str, Component]


@dataclass
class WorldSave:
    world_id: str
    buildable: np.ndarray
    area_registry: Dict[Tuple[int, int], AreaData]


class GameData:

    def __init__(self):
        self._character: Optional[CharacterSave] = None
        self._world: Optional[WorldSave] = None
        self.save_id = None

    @property
    def world(self) -> WorldSave:
        return self._world

    @world.setter
    def world(self, world: WorldSave) -> None:
        self._world = world
        self.save_id = self._world.world_id + "_" + str(datetime.date.today())

    @property
    def character(self) -> CharacterSave:
        return self._character

    @character.setter
    def character(self, character: CharacterSave) -> None:
        self._character = character

    def __str__(self) -> str:
        if self._world:
            if self._character:
                return f"WORLD: {self._world.world_id}; CHARACTER: {self._character}"
            return f"WORLD: {self._world.world_id}; CHARACTER: None"
        return f"WORLD: None; Character: None"


class Storage:

    @staticmethod
    def add_character(game_data: GameData, character: CharacterSave) -> None:
        game_data.character = character

    @staticmethod
    def load_character(game_data: GameData) -> CharacterSave:
        return game_data.character

    @staticmethod
    def add_world(game_data: GameData, world: WorldSave) -> None:
        for area in world.area_registry.values():
            area.tile_map.actors = None
        game_data.world = world

    @staticmethod
    def load_world(game_data: GameData) -> WorldSave:
        return game_data.world

    @staticmethod
    def write_to_file(data: GameData) -> None:
        Manifest.update(data)
        save_data = pickle.dumps(data, protocol=4)
        with open(get_save(Manifest.data["saves"][data.save_id]), "wb") as f:
            f.write(save_data)

    @staticmethod
    def load_from_file(file: str) -> GameData:
        try:
            _file = Manifest.data["saves"][file]
            with open(get_save(_file), "rb") as f:
                data = pickle.loads(f.read())
                return data
        except Exception:
            traceback.print_exc(file=sys.stderr)
