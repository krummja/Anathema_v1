from __future__ import annotations
from math import floor, ceil
from random import randint
import numpy as np

import tcod
from tcod.loader import lib, ffi

from anathema.engine.world.planet.tcod_heightmap import *


class Heightmap:

    def __init__(self, width: int, height: int) -> None:
        self._array = heightmap_new(height, width, order="C")

    @property
    def array(self) -> np.ndarray:
        return self._array

    @property
    def width(self):
        return self._array.shape[0]

    @property
    def height(self):
        return self._array.shape[1]

    def add_mountains(self, count: int):
        for i in range(count):
            heightmap_add_hill(
                self._array,
                randint(self.height // 10, self.height - self.height // 10),
                randint(self.width // 10, self.width - self.width // 10),
                randint(12, 16), randint(6, 10)
            )

    def add_hills(self, count: int):
        for i in range(count):
            heightmap_add_hill(
                self._array,
                randint(self.height // 10, self.height - self.height // 10),
                randint(self.width // 10, self.width - self.width // 10),
                randint(2, 4), randint(6, 10)
            )

    def apply_simplex_noise(self):
        _noise = heightmap_new(self.height, self.width)
        noise_2d = tcod.noise.Noise(
            dimensions = 2,
            algorithm = tcod.noise.Algorithm.SIMPLEX,
            implementation = tcod.noise.Implementation.SIMPLE,
            hurst = 0.8,
            lacunarity = 1.2,
            octaves = 4.0
        )

        heightmap_add_fbm(_noise, noise_2d, 6, 6, 0, 0, 32, 1, 1)
        heightmap_normalize(_noise, 0.0, 1.0)
        heightmap_multiply_hm(self._array, _noise, self._array)

    def normalize(self):
        heightmap_normalize(self._array, 0.0, 1.0)

    def clamp(self):
        heightmap_clamp(self._array, 0.0, 1.0)

    def rain_erode(self):
        heightmap_rain_erosion(self._array, self.width * self.height, 0.07, 0)
        heightmap_clamp(self._array, 0.0, 1.0)

    @staticmethod
    def point_distance_round(x1: int, y1: int, x2: int, y2: int) -> int:
        return round( abs(x2 - x1) + abs(y2 - y1) )

    def lowest_neighbor(self, world, x: int, y: int):
        min_val: int = 1
        _x: int = 0
        _y: int = 0

        if world[x + 1][y] < min_val and x + 1 < self.width:
            min_val = world[x + 1][y]
            _x, _y = x + 1, y

        if world[x][y + 1] < min_val and y + 1 < self.height:
            min_val = world[x][y + 1]
            _x, _y = x, y + 1

        if world[x - 1][y] < min_val and x - 1 > 0:
            min_val = world[x - 1][y]
            _x, _y = x - 1, y

        if world[x][y - 1] < min_val and y - 1 > 0:
            min_val = world[x][y - 1]
            _x, _y = x, y - 1

        error = 0
        if x == 0 and y == 0:
            error = 1
        return _x, _y, error
