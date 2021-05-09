from __future__ import annotations
from typing import *
from anathema.data import Storage

if TYPE_CHECKING:
    from anathema.data import GameData, CharacterSave, WorldSave, WorldData


class Session:

    def __init__(self):
        self._data: Optional[GameData] = None
        self.character_data: Optional[CharacterSave] = None
        self.world_data: Optional[WorldSave] = None

    @property
    def data(self) -> GameData:
        return self._data

    @data.setter
    def data(self, value: GameData) -> None:
        self._data = value
        self.character_data = Storage.load_character(self._data)
        self.world_data = Storage.load_world(self._data)
