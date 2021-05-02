from __future__ import annotations
from typing import *

from morphism import *
import tcod.map
from tcod.color import Color

from anathema.engine.core import BaseManager
from anathema.engine.world.area import Area
from anathema.engine.world.tile import Tile
from anathema.engine.world.generation.array_tools import rng_selection
from anathema.engine.world.generation.automata import *
from anathema.engine.world.planet.generator import PlanetView, PlanetGenerator
from anathema.engine.world.generation.color import test_palette

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class TestArea(Area):

    name: str = "Test"

    def __init__(self):
        super().__init__(512, 512)

    def initialize(self):
        automata = Anneal((512, 512), density=0.46)
        automata.generate(10)
        result = automata.board
        result = np.where(result == 1, self._factory.dirt_1.make(), self._factory.unformed.make())
        self._tiles[:] = result

        self._tiles = rng_selection(
            self._tiles,
            self._factory.unformed,
            self._factory.dirt_2,
            [(10, self._factory.tree_1),
             (20, self._factory.grass),
             (40, self._factory.tall_grass)]
        )

        # TODO Make a helper function for room construction...
        room = Rect(Point(5, 5), Size(8, 8))
        self._tiles[room.outer] = self._factory.flagstone_wall.make()
        self._tiles[room.inner] = self._factory.flagstone_floor.make()
        self._tiles[room.bottom-1, 8] = self._factory.flagstone_floor.make()


class WorldManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.current_area = None
        self.generator = PlanetGenerator(130, 200)
        self.planet_view = PlanetView(self.generator)

    def initialize_world(self):
        self.generator.generate()
        self.planet_view.generate_view(test_palette)

    def initialize(self):
        self.current_area = TestArea()
        self.current_area.initialize()
