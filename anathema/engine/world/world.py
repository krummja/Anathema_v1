from __future__ import annotations
from typing import *

from .region import Region

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class World:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.regions = {}
        self._current_region = None

    @property
    def current_region(self) -> Region:
        return self._current_region

    def add_region(self, region: Region):
        self.regions[region.name] = region(self)
