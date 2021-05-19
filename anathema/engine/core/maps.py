from __future__ import annotations
from typing import *

import numpy as np
from morphism import *
import tcod.map
from tcod.color import Color

from anathema.engine.core import BaseManager
from anathema.engine.world.tilemap import TileMap
from anathema.engine.world.tile import Tile
from anathema.engine.world.generation.array_tools import rng_selection
from anathema.engine.world.generation.automata import *
from anathema.engine.world.planet.generator import PlanetView, PlanetGenerator
from anathema.engine.core.options import Options
from anathema.engine.world.generation.schemata.structure import StructureScheme, Themes
from anathema.engine.world.generation.room_builder import RoomBuilder
from anathema.data import *
from anathema.engine.world.generation.components import world_components

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class TestArea(TileMap):

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
        result = np.where(result == 1, self._tile_registry.dirt_2.make(), self._tile_registry.unformed.make())
        self._tiles[:] = result

        self._tiles = rng_selection(
            self._tiles,
            self._tile_registry.unformed,
            self._tile_registry.dirt_2,
            [(10, self._tile_registry.tree_1),
             (20, self._tile_registry.grass),
             (40, self._tile_registry.tall_grass)]
        )

        self._tiles[246:266+10, 246:266] = self._tile_registry.dirt_2.make()
        room_mask = StructureScheme.generate()
        room_struct = StructureScheme.populate(room_mask, "flagstone")
        self._tiles = StructureScheme.plop(room_struct, (250, 250), self._tiles)


class AreaData:

    def __init__(self, index: Tuple[int, int], tile_map: TileMap):
        self.index = index
        self.tile_map = tile_map
        self.connections = {}


class WorldData:

    def __init__(self, world_id: str):
        self.world_id = world_id
        self.buildable = np.ones((Options.WORLD_HEIGHT, Options.WORLD_WIDTH), dtype=bool)
        self.area_registry = {}

    def new_area(self, position: Tuple[int, int], tile_map: Optional[TileMap] = None):
        x, y = position
        if self.buildable[y, x]:
            tile_map.initialize()
            area = AreaData((y, x), tile_map)
            self.buildable[y, x] = False
            self.area_registry[area.index] = area

    def get_area_data(self, x: int, y: int):
        return self.area_registry[(x, y)].tile_map


class MapManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.engine = self.game.ecs.engine
        self.world = self.game.ecs.world
        self.current_area: Optional[TileMap] = None
        # self.generator = PlanetGenerator(Options.WORLD_HEIGHT, Options.WORLD_WIDTH)
        # self.planet_view = PlanetView(self.generator)

    def initialize(self):
        self.current_area = TestArea()
        self.current_area.initialize()

    def teardown(self):
        self.current_area = None

    def _register_components(self):
        for component in world_components():
            self.engine.register_component(component)
