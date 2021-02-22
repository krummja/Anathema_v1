from __future__ import annotations
from typing import Tuple, List, TYPE_CHECKING

import numpy as np

from anathema.utils.geometry import Rect, Point, Size
from anathema.world.tiles import Tiles
from anathema.world.generation.cellular import *

if TYPE_CHECKING:
    from anathema.world.tile_type import TileType


class TileSpace:

    @staticmethod
    def initialize():
        tile_space = np.zeros((64, 64), dtype=object, order="F")

        #! Point where specific generators may intervene.

        automata = Anneal((64, 64), density=0.46)
        automata.generate(10)
        result = automata.board

        result = np.where(result == 1, Tiles.unformed_wet(), Tiles.unformed())
        tile_space[:] = result

        TileSpace.rng_selection(
            tile_space,
            Tiles.unformed(),
            Tiles.dirt_2(),
            [(10, Tiles.tree_1()), (20, Tiles.grass()), (40, Tiles.tall_grass())])

        # outdoor_tiles = np.full(100, fill_value=Tiles.dirt_2())
        # outdoor_tiles[:10] = Tiles.tree_1()
        # outdoor_tiles[10:20] = Tiles.grass()
        # outdoor_tiles[20:40] = Tiles.tall_grass()

        # is_unformed = (tile_space == Tiles.unformed())
        # rng_samples = np.random.randint(low=0, high=100, size=(64, 64))
        # np.putmask(tile_space, is_unformed, outdoor_tiles[rng_samples])

        # tile_space[16:25, 16:25] = Tiles.unformed_wet()
        # tile_space[18:23, 18:23] = Tiles.solid_wet()

        # room = Rect(Point(5, 5), Size(10, 10))
        # tile_space[room.outer] = Tiles.flagstone_wall()
        # tile_space[room.inner] = Tiles.flagstone_floor()
        # tile_space[room.top_left.x+3:room.top_left.x+6, room.top] = Tiles.flagstone_floor()

        return tile_space

    @staticmethod
    def rng_selection(
            tile_space: TileSpace,
            mask_type: TileType,
            fill_type: TileType,
            asset_list: List[Tuple[int, TileType]]
        ) -> TileSpace:
        """Takes in the TileSpace, a fill TileType, and a list of (threshold, TileType)
        pairs to map to the selection set.

        e.g.    [(10, Tiles.tree_1()), (20, Tiles.grass()), (40, Tiles.tall_grass())]
             => selection_set[  :10] = Tiles.tree_1()
             => selection_set[10:20] = Tiles.grass()
             => selection_set[20:40] = Tiles.tall_grass()
        """
        selection_set = np.full(100, fill_value=fill_type)
        low = 0
        for threshold, tile_type in asset_list:
           selection_set[low:threshold] = tile_type
           low = threshold

        mask = (tile_space == mask_type)
        rng_samples = np.random.randint(low=0, high=100, size=(64, 64))
        np.putmask(tile_space, mask, selection_set[rng_samples])
        return tile_space
