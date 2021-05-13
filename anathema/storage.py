from __future__ import annotations
from typing import *
import os
import json
import pickle

if TYPE_CHECKING:
    from anathema.engine.core.session import Session
    from anathema.data import GameData, WorldSave


ROOT_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(ROOT_DIR, "_assets")
SAVE_DIR = os.path.join(ROOT_DIR, "_saves")
CONTENT_DIR = os.path.join(ROOT_DIR, "content")
MANIFEST = os.path.join(SAVE_DIR, "manifest.json")


def get_data(path: str) -> str:
    assert os.path.exists(ASSET_DIR), f"Cannot find asset path: {ASSET_DIR}"
    return os.path.join(ASSET_DIR, path)


def get_save(path: str) -> str:
    assert os.path.exists(SAVE_DIR), f"Cannot find save path: {SAVE_DIR}"
    return os.path.join(SAVE_DIR, path)


class Storage:
    """High-level interface that handles loading GameData from file
    to bind to Session and saving Session data to file.

    Only Storage may lock or unlock the Session's data.
    """

    _manifest = {}

    @staticmethod
    def manifest_entries():
        return Storage._manifest.keys()

    @staticmethod
    def write_to_file(session: Session) -> None:
        Storage.update_manifest(session.data)
        save_data = pickle.dumps(session.data, protocol=4)
        with open(get_save(Storage._manifest[session.data.save_id]), "wb") as f:
            f.write(save_data)

    @staticmethod
    def load_from_file(session: Session, file: str) -> None:
        session.unlock()
        session.clear()
        with open(get_save(Storage._manifest[file]), "rb") as f:
            save_data = pickle.loads(f.read())
        session.data = save_data
        session.lock()

    @staticmethod
    def write_to_manifest():
        with open(MANIFEST, "w") as manifest:
            json.dump(Storage._manifest, manifest)

    @staticmethod
    def load_from_manifest():
        if not os.path.exists(MANIFEST):
            with open(MANIFEST, "w") as manifest:
                json.dump(Storage._manifest, manifest)
        with open(MANIFEST, "r") as manifest:
            Storage._manifest = json.load(manifest)

    @staticmethod
    def update_manifest(data: GameData):
        Storage._manifest.update({data.save_id: data.save_id + ".sav"})
        Storage.write_to_manifest()

    @staticmethod
    def delete_from_manifest(save_id: str):
        del Storage._manifest[save_id]
        Storage.write_to_manifest()

    @staticmethod
    def new_game_setup(session: Session, world_save: WorldSave):
        session.unlock()
        if session.data is not None:
            Storage.write_to_file(session)
        session.clear()
        session.new_game(world_save)
        Storage.write_to_file(session)
        session.lock()

    @staticmethod
    def delete_world(session: Session):
        session.unlock()
        save_id = session.data.save_id
        os.remove(os.path.join(SAVE_DIR, save_id + ".sav"))
        session.delete()
        session.lock()

    @staticmethod
    def delete_character(session: Session):
        session.unlock()
        session.delete_character()
        Storage.write_to_file(session)
        session.lock()
