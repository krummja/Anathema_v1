from __future__ import annotations
from typing import *
import os
import datetime
import pickle
import json

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core.game import Game
    from ecstremity import World


ROOT_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(ROOT_DIR, "assets")
DATA_DIR = os.path.join(ROOT_DIR, "engine/data")
SAVE_DIR = os.path.join(ROOT_DIR, "savedata")
MANIFEST = os.path.join(SAVE_DIR, "manifest.json")


def get_data(path: str) -> str:
    assert os.path.exists(ASSET_DIR), f"Cannot find asset path: {ASSET_DIR}"
    return os.path.join(ASSET_DIR, path)


def get_save(path: str) -> str:
    assert os.path.exists(SAVE_DIR), f"Cannot find save path: {SAVE_DIR}"
    return os.path.join(SAVE_DIR, path)


class SaveData:

    def __init__(self, save_id: str, player_uid: str, world: World) -> None:
        self.save_id = save_id
        self.player_uid = player_uid
        self.world = world


class Storage(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._manifest = {}

    @property
    def manifest_entries(self):
        return self._manifest.keys()

    def write_to_file(self) -> None:
        save_package = self._package_save_data()
        self._update_manifest(save_package)

        save_data = pickle.dumps(save_package, protocol=4)
        with open(get_save(self._manifest[save_package.save_id]), "wb") as stream:
            stream.write(save_data)

    def read_from_file(self, file: str):
        with open(get_save(self._manifest[file]), "rb") as stream:
            save_data = pickle.loads(stream.read())
            self._unpackage_save_data(save_data)
            player = self.game.ecs.world.get_entity(save_data.player_uid)
            return player

    def read_from_manifest(self) -> None:
        if not os.path.exists(MANIFEST):
            self._write_to_manifest()
        with open(MANIFEST, "r") as manifest:
            self._manifest = json.load(manifest)

    def _package_save_data(self) -> SaveData:
        save_id = self._make_save_id()
        player_uid = self.game.player.uid
        world_data = self.game.ecs.world.serialize()
        return SaveData(save_id, player_uid, world_data)

    def _unpackage_save_data(self, data: SaveData) -> None:
        self.game.ecs.world.deserialize(data.world)

    def _write_to_manifest(self) -> None:
        with open(MANIFEST, "w") as manifest:
            json.dump(self._manifest, manifest)

    def _update_manifest(self, data: SaveData) -> None:
        self._manifest.update({data.save_id: data.save_id + ".sav"})
        self._write_to_manifest()

    def _delete_from_manifest(self, save_id: str) -> None:
        del self._manifest[save_id]
        self._write_to_manifest()

    @staticmethod
    def _make_save_id() -> str:
        save_id = str(datetime.date.today())
        return save_id
