from __future__ import annotations
from typing import *

import datetime
from anathema.storage import Storage
from anathema.data import GameData

if TYPE_CHECKING:
    from anathema.data import WorldSave, CharacterSave
    from ecstremity import Component


class Session:

    def __init__(self):
        """Data for a single game session.

        The Session class holds reference to a single GameData object.
        While the Session object is locked, its values are readonly.
        """
        self.locked = True
        self._data: Optional[GameData] = None

    @property
    def data(self) -> GameData:
        return self._data

    @data.setter
    def data(self, value: GameData) -> None:
        if not self.locked:
            self._data = value
        else:
            print("Session data instance is readonly while locked!")

    def lock(self):
        if not self.locked:
            self.locked = True

    def unlock(self):
        if self.locked:
            self.locked = False

    def clear(self):
        if not self.locked:
            self._data = None
        else:
            print("Session data instance is readonly while locked!")

    def delete(self):
        if not self.locked:
            save_id = self.data.save_id
            self._data = None
            Storage.delete_from_manifest(save_id)
        else:
            print("Session data instance is readonly while locked!")

    def delete_character(self):
        if not self.locked:
            self._data.character_save = None
        else:
            print("Session data instance is readonly while locked!")

    def new_game(self, world_save: WorldSave) -> None:
        if not self.locked:
            save_id = world_save.world_id + "_" + str(datetime.date.today())
            self.data = GameData(save_id, world_save)

