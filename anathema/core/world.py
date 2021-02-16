from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Optional

from anathema.abstracts import AbstractManager
from anathema.world.area import Area
from anathema.world.region import Region

if TYPE_CHECKING:
    from anathema.core import Game


class WorldManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.ecs = game.ecs.engine
        self.regions: Dict[str, Dict[str, Area]] = {
            'start': Region('start', self)
            }

        # TODO Replace this with a more robust generation system eventually
        self.regions['start'].add_area('test area')

        self._current_region = self.regions['start']
        self._current_area: Optional[Area] = None
        self.set_area('test area')

    @property
    def current_area(self) -> Area:
        return self._current_area

    def set_area(self, area: str) -> None:
        self._current_area = self.regions[self._current_region.name].areas[area]
