from __future__ import annotations
import numpy as np
from typing import *

from anathema.world.tiles import Tiles
from anathema.world.tile_space import TileSpace


class TestSpace(TileSpace):

    def __init__(self, size):
        super().__init__(size)

    def initialize(self):
        tile_space = np.zeros(self.size, dtype=object, order="F")
        tile_space[:] = Tiles.dirt_1
        tile_space[8, 8] = Tiles.closed_chest
        return tile_space
