from __future__ import annotations
from typing import *
from morphism import *
from contextlib import contextmanager
import numpy as np

from anathema.engine.core import BaseManager
from anathema.engine.world.tile import tile_graphic

if TYPE_CHECKING:
    from anathema.engine.core.game import Game
    from anathema.engine.world.tilemap import TileMap
    from anathema.engine.world.planet.generator import PlanetView


class RenderManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.root_console = self.game.console.root

    def render_area_tiles(self, area: TileMap) -> None:
        screen_view, world_view = self.game.camera.camera_view(area.width, area.height)
        self.root_console.tiles_rgb[screen_view] = self.select_area_mask(area, world_view)

    def render_world_map(self, planet_view: PlanetView) -> None:
        screen_view, world_view = self.game.camera.camera_view(planet_view.width, planet_view.height)
        self.root_console.tiles_rgb[screen_view] = self.select_world_view(planet_view, world_view)

    @staticmethod
    def select_area_mask(area: TileMap, world_view: Tuple[slice, slice]) -> np.ndarray:
        UNKNOWN = np.asarray((0, (21, 21, 21), (21, 21, 21)), dtype=tile_graphic)

        if_visible = area.visible[world_view]
        if_explored = area.explored[world_view]
        lit_tiles = area.tiles["light"][world_view]
        unlit_tiles = area.tiles["dark"][world_view]

        condlist = (if_visible, if_explored)
        choicelist = (lit_tiles, unlit_tiles)

        return np.select(condlist, choicelist, UNKNOWN)

    @staticmethod
    def select_world_view(planet_view: PlanetView, world_view: Tuple[slice, slice]) -> np.ndarray:
        return planet_view.view[world_view]
