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

        # TODO Break this out into a method
        automata = Anneal((64, 64), density=0.46)
        automata.generate(10)
        result = automata.board
        result = np.where(result == 1, Tiles.shallow_water, Tiles.unformed)
        tile_space[:] = result

        TileSpace.rng_selection(
            tile_space,
            Tiles.unformed,
            Tiles.dirt_2,
            [(10, Tiles.tree_1), (20, Tiles.grass), (40, Tiles.tall_grass)])

        # TODO Break this out into a method
        room = Rect(Point(5, 5), Size(10, 10))
        tile_space[room.outer] = Tiles.flagstone_wall
        tile_space[room.inner] = Tiles.flagstone_floor
        tile_space[room.top_left.x+4, room.top] = Tiles.closed_door
        tile_space[room.right-1, room.top+4] = Tiles.closed_door

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
