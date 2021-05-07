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
from anathema.engine.core.options import Options
from anathema.engine.world.generation.room_builder import RoomBuilder

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class TestArea(Area):

    name: str = "Test"

    def __init__(self):
        super().__init__(512, 512)
        self.room_builder = RoomBuilder(
            max_rooms = 10,
            min_size = 8,
            max_size = 12
        )

    def initialize(self):
        automata = Anneal((512, 512), density=0.46)
        automata.generate(10)
        result = automata.board
        result = np.where(result == 1, self._factory.shallow_water.make(), self._factory.unformed.make())
        self._tiles[:] = result

        self._tiles = rng_selection(
            self._tiles,
            self._factory.unformed,
            self._factory.dirt_2,
            [(10, self._factory.tree_1),
             (20, self._factory.grass),
             (40, self._factory.tall_grass)]
        )

        # for room in self.room_builder.execute(10, 10, 100, 100):
        #     self._tiles[room.outer] = self._factory.flagstone_wall.make()
        #     self._tiles[room.inner] = self._factory.flagstone_floor.make()
        #     self._tiles[room.bottom-1, 8] = self._factory.flagstone_floor.make()

        self._tiles[0:40, 0:40] = self._factory.dirt_1.make()
        room = Rect(Point(1, 1), Size(5, 5))
        self._tiles[room.outer] = self._factory.flagstone_wall.make()
        self._tiles[room.inner] = self._factory.flagstone_floor.make()
        self._tiles[room.bottom-1, room.point_bottom_right.x - 2] = self._factory.flagstone_floor.make()


class WorldManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.current_area: Optional[Area] = None
        self.generator = PlanetGenerator(Options.WORLD_HEIGHT, Options.WORLD_WIDTH)
        self.planet_view = PlanetView(self.generator)

    def initialize_world(self):
        self.generator.generate()

    def initialize_region(self):
        pass

    def initialize_area(self):
        self.current_area = TestArea()
        self.current_area.initialize()

    def initialize(self):
        self.initialize_region()
        self.initialize_area()
