from __future__ import annotations
from typing import *
import numpy as np

if TYPE_CHECKING:
    from anathema.engine.world.generation.tiles import TileType


def rng_selection(
        tile_array: np.ndarray,
        mask_type: TileType,
        fill_type: TileType,
        asset_list: List[Tuple[int, TileType]]
    ) -> np.ndarray:
    """Takes in the TileSpace, a fill TileType, and a list of (threshold, TileType)
    pairs to map to the selection set.
    e.g.    [(10, Tiles.tree_1()), (20, Tiles.grass()), (40, Tiles.tall_grass())]
         => selection_set[  :10] = Tiles.tree_1()
         => selection_set[10:20] = Tiles.grass()
         => selection_set[20:40] = Tiles.tall_grass()
    """
    selection_set = np.full(100, fill_value=fill_type.make())
    low = 0
    for threshold, tile_type in asset_list:
        selection_set[low:threshold] = tile_type.make()
        low = threshold

    mask = (tile_array == mask_type.make())
    rng_samples = np.random.randint(low=0, high=100, size=(512, 512))
    np.putmask(tile_array, mask, selection_set[rng_samples])
    return tile_array
