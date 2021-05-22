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


class MapManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.engine = self.game.ecs.engine
        self.world = self.game.ecs.world
        self.current_area = None
        self._register_components()

    @property
    def actors(self):
        return self.entity['Map_Actors'].actors

    @property
    def entity(self):
        return self.current_area.entity

    @property
    def tiles(self):
        return self.current_area

    def initialize(self):
        area = self.world.create_entity()
        area.add('Map_Moniker', {'name': 'Test Area'})
        area.add('Map_Tilemap', {'width': 512, 'height': 512})
        area.add('Map_WorldLocation', {'x': 0, 'y': 0})
        area.add('Map_Actors', {})
        area.add('Map_Terrain', {})
        self.current_area = area['Map_Tilemap']

    def teardown(self):
        self.current_area = None

    def _register_components(self):
        for component in world_components():
            self.engine.register_component(component)
