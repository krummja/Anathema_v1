from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Optional

from anathema.core.base_manager import BaseManager
from anathema.world.area import Area
from anathema.world.region import Region
from anathema.data.areas.test_area import TestArea

if TYPE_CHECKING:
    from anathema.core.game import Game


class WorldManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.ecs = game.ecs.engine
        self.regions = {}
        self._current_area = None
        self._current_region = None

    def initialize(self):
        self.regions: Dict[str, Region] = {
            'start': Region('start', self)
            }

        self.regions['start'].add_area(TestArea)

        self._current_region = self.regions['start']
        self._current_area: Optional[Area] = None
        self.set_area('Test Area')

    @property
    def current_area(self) -> Area:
        return self._current_area

    def set_area(self, area: str) -> None:
        self._current_area = self.regions[self._current_region.name].areas[area]
