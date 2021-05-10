from __future__ import annotations
from typing import *
from anathema.data import Storage

from anathema.data import GameData, WorldSave

if TYPE_CHECKING:
    from anathema.data import CharacterSave, WorldData


class Session:

    def __init__(self):
        """Data for a single game session.

        The Session class holds reference to a single GameData object.
        Every GameData object has only one WorldSave and one CharacterSave.
        """
        self._data: Optional[GameData] = None
        self.world_data: Optional[WorldSave] = None
        self.character_data: Optional[CharacterSave] = None

    @property
    def game_data(self) -> GameData:
        return self._data

    @game_data.setter
    def game_data(self, value: GameData) -> None:
        self._data = value

    def new_game_data(self):
        """Create a new GameData object."""
        self._data = GameData()

    def new_world_data(self, world_data: WorldData):
        """Add WorldData object from WorldGen, then add it to the session."""
        world_save = WorldSave(
            world_id = world_data.world_id,
            buildable = world_data.buildable,
            area_registry = world_data.area_registry,
        )
        self.world_data = world_data
        self._data.world = world_save

    def load_game_data(self):
        """Load all data from the session's GameData into memory."""
        if self._data:
            print("Found save file...")
            if self._data.world:
                print("Loaded world data.")
                self.world_data = self._data.world
            if self._data.character:
                print("Loaded character data.")
                self.character_data = self._data.character
