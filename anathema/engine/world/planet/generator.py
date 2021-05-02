from __future__ import annotations
from typing import *
from random import randint, uniform
import numpy as np
import tcod
from anathema.engine.world.planet.heightmap import *
from anathema.engine.world.tile import tile_graphic

if TYPE_CHECKING:
    pass


world_tile = np.dtype([
    ("height", np.float32),
    ("temperature", np.float32),
    ("precipitation", np.float32),
    ("drainage", np.float32),
    ("biome_id", np.uint8),
    ("has_river", np.bool),
])


class PlanetGenerator:

    def __init__(
            self,
            height: int,
            width: int,
        ) -> None:
        self.width = width
        self.height = height
        self.heightmap = Heightmap(height, width)
        self.world_data = np.zeros((width, height), world_tile)

    def generate(self):
        self.initialize_map()
        self.pole_generator(0)
        self.pole_generator(1)
        self.tectonic_generator(0)
        self.tectonic_generator(1)
        self.heightmap.rain_erode()
        self.initialize_world_data()
        self.river_gen()

    def initialize_world_data(self):
        # initialize temperature
        # initialize precipitation
        # initialize drainage
        for x in range(self.width):
            for y in range(self.height):
                self.world_data[x][y] = (heightmap_get_value(self.heightmap._array, x, y), 0, 0, 0, 0, 0)

                if (0.10 <= self.world_data[x][y]["precipitation"] < 0.33
                        and self.world_data[x][y]["drainage"] < 0.5
                    ):
                    self.world_data[x][y]["biome_id"] = 3
                    if randint(1, 2) == 2:
                        self.world_data[x][y]["biome_id"] = 16

                if (self.world_data[x][y]["precipitation"] >= 0.10
                        and self.world_data[x][y]["precipitation"] > 0.33
                    ):
                    self.world_data[x][y]["biome_id"] = 2
                    if self.world_data[x][y]["precipitation"] >= 0.66:
                        self.world_data[x][y]["biome_id"] = 1

                if (0.33 <= self.world_data[x][y]["precipitation"] < 0.66
                        and self.world_data[x][y]["drainage"] >= 0.33
                    ):
                    self.world_data[x][y]["biome_id"] = 15
                    if randint(1, 5) == 5:
                        self.world_data[x][y]["biome_id"] = 5

                if (self.world_data[x][y]["temperature"] > 0.2
                        and self.world_data[x][y]["precipitation"] >= 0.66
                        and self.world_data[x][y]["drainage"] > 0.33
                    ):
                    self.world_data[x][y]["biome_id"] = 5
                    if self.world_data[x][y]["precipitation"] >= 0.75:
                        self.world_data[x][y]["biome_id"] = 6
                    if randint(1, 5) == 5:
                        self.world_data[x][y]["biome_id"] = 15

                if (0.10 <= self.world_data[x][y]["precipitation"] < 0.33
                        and self.world_data[x][y]["drainage"] >= 0.5
                    ):
                    self.world_data[x][y]["biome_id"] = 16
                    if randint(1, 2) == 2:
                        self.world_data[x][y]["biome_id"] = 14

                if self.world_data[x][y]["precipitation"] < 0.10:
                    self.world_data[x][y]["biome_id"] = 4
                    if self.world_data[x][y]["drainage"] > 0.5:
                        self.world_data[x][y]["biome_id"] = 16
                        if randint(1, 2) == 2:
                            self.world_data[x][y]["biome_id"] = 14

                    if self.world_data[x][y]["drainage"] >= 0.66:
                        self.world_data[x][y]["biome_id"] = 8

                if self.world_data[x][y]["height"] <= 0.2:
                    self.world_data[x][y]["biome_id"] = 0

                if (self.world_data[x][y]["temperature"] <= 0.2
                        and self.world_data[x][y]["height"] > 0.15
                    ):
                    self.world_data[x][y]["biome_id"] = randint(11, 13)

                if self.world_data[x][y]["height"] > 0.6:
                    self.world_data[x][y]["biome_id"] = 9
                if self.world_data[x][y]["height"] > 0.9:
                    self.world_data[x][y]["biome_id"] = 10

    def initialize_map(self):
        self.heightmap.add_mountains(250)
        self.heightmap.add_hills(1000)
        self.heightmap.normalize()
        self.heightmap.apply_simplex_noise()

    def pole_generator(self, ns: int):
        if ns == 0:
            rng = randint(2, 5)
            for i in range(self.width):  # across the entire width of the map ...
                for j in range(rng):     # at random distances from the map edge ...
                    heightmap_set_value(self.heightmap._array, i, self.height - 1 - j, 0.31)
                rng += randint(1, 3) - 2
                rng = min(max(2, rng), 5)

        if ns == 1:
            rng = randint(2, 5)
            for i in range(self.width):
                for j in range(rng):
                    heightmap_set_value(self.heightmap._array, i, j, 0.31)
                rng += randint(1, 3) - 2
                rng = min(max(2, rng), 5)

    def tectonic_generator(self, hor):
        tectonic_tiles = [[0 for _ in range(self.height)] for _ in range(self.width)]
        if hor == 1:
            pos = randint(self.height // 10, self.height - self.height // 10)
            for x in range(self.width):
                tectonic_tiles[x][pos] = 1
                pos += randint(1, 5) - 3
                pos = min(max(0, pos), self.height - 1)

        if hor == 0:
            pos = randint(self.width // 10, self.width - self.width // 10)
            for y in range(self.height):
                tectonic_tiles[pos][y] = 1
                pos += randint(1, 5) - 3
                pos = min(max(0, pos), self.width - 1)

        for x in range(self.width // 10, self.width - self.width // 10):
            for y in range(self.height // 10, self.height - self.height // 10):
                if tectonic_tiles[x][y] == 1 and heightmap_get_value(self.heightmap._array, x, y) > 0.3:
                    heightmap_add_hill(self.heightmap._array, x, y, randint(2, 4), uniform(0.15, 0.18))

    def temperature(self):
        for x in range(self.width):
            for y in range(self.height):
                height_effect = 0
                if y > self.height / 2:
                    heightmap_set_value(temp, x, y, self.height - y - height_effect)
                else:
                    heightmap_set_value(temp, x, y, y - height_effect)
                height_effect = heightmap_get_value(self.heightmap._array, x, y)

                if height_effect > 0.8:
                    height_effect *= 5
                    if y > self.height / 2:
                        heightmap_set_value(temp, x, y, self.height - y - height_effect)
                    else:
                        heightmap_set_value(temp, x, y, y - height_effect)

                if height_effect < 0.25:
                    height_effect *= 10
                    if y > self.height / 2:
                        heightmap_set_value(temp, x, y, self.height - y - height_effect)
                    else:
                        heightmap_set_value(temp, x, y, y - height_effect)

    def river_gen(self):
        MIN_RIVER_LENGTH = 10
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        _x = []
        _y = []
        tries = 0

        while self.world_data[x][y]["height"] < 0.8:
            tries += 1
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            if tries > 2000:
                return

        del _x[:]
        del _y[:]

        _x.append(x)
        _y.append(y)

        while self.world_data[x][y]["height"] >= 0.2:
            x, y, error = self.heightmap.lowest_neighbor(self.heightmap._array, x, y)
            if error == 1:
                return
            try:
                if (
                    self.world_data[x][y]["has_river"] or
                    self.world_data[x+1][y]["has_river"] or
                    self.world_data[x-1][y]["has_river"] or
                    self.world_data[x][y+1]["has_river"] or
                    self.world_data[x][y-1]["has_river"]
                ):
                    return
            except IndexError:
                break

            if x in _x and y in _y:
                break

            _x.append(x)
            _y.append(y)

        if len(_x) <= MIN_RIVER_LENGTH:
            return

        for i, _ in enumerate(_x):
            if self.world_data[_x[i]][_y[i]]["height"] < 0.2:
                break
            self.world_data[_x[i]][_y[i]]["has_river"] = True
            if self.world_data[_x[i]][_y[i]]["height"] >= 0.2 and i == len(_x):
                self.world_data[_x[i]][_y[i]]["has_river"] = True


class CivilizationGenerator:

    def __init__(self):
        pass


class PlanetView:

    def __init__(self, generator: PlanetGenerator) -> None:
        """Constructs viewable arrays for the planet generator.

        world_data      ndarray<world_tile>
                        - height          np.float32
                        - temperature     np.float32
                        - precipitation   np.float32
                        - drainage        np.float32
                        - biome_id        np.uint8
        """
        self.generator = generator
        self.world_data = generator.world_data
        self.view = np.zeros((self.height, self.width), tile_graphic, order="F")

    @property
    def width(self):
        return self.generator.width

    @property
    def height(self):
        return self.generator.height

    def generate_view(self):
        palette = [
            tcod.Color(25, 255, 25),
            tcod.Color(25, 200, 25),
            tcod.Color(25, 150, 25),
            tcod.Color(25, 100, 25),
            tcod.Color(25, 50, 25),
            tcod.Color(25, 25, 25),
        ]

        self.view[:] = (ord("0"), tcod.blue, (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.1] = (ord("1"), tcod.blue, (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.2] = (ord("2"), palette[0], (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.3] = (ord("3"), palette[1], (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.4] = (ord("4"), palette[2], (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.5] = (ord("5"), palette[3], (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.6] = (ord("6"), palette[4], (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.7] = (ord("7"), palette[5], (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.8] = (ord("8"), tcod.dark_sepia, (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.9] = (ord("9"), tcod.light_gray, (0x15, 0x15, 0x15))
        self.view.T[self.world_data["height"] > 0.99] = (ord("^"), tcod.lighter_gray, (0x15, 0x15, 0x15))

    # def generate_view(self):
    #     """Takes world_data and maps it to view based on mapping presets."""
    #     self.view[:] = (ord("0"), (0x00, 0xFF, 0x00), (0x15, 0x15, 0x15))
    #     thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
    #
    #     # TODO Extract this to some separate utility method
    #     symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "^"]
    #     symbol_list = [ord(symbol) for symbol in symbols]
    #     foreground_list = [(0x00, 0xFF, 0x00)] * len(symbol_list)
    #     background_list = [(0x15, 0x15, 0x15)] * len(symbol_list)
    #     renderables = list(zip(symbol_list, foreground_list, background_list))
    #
    #     low = 0.0
    #     for i, threshold in enumerate(thresholds):
    #         condition = (low < self.world_data["height"].any()) & (self.world_data["height"].any() <= threshold)
    #         if condition:
    #             renderable = renderables[i]
    #             self.view.T[np.transpose(np.nonzero(condition))] = renderable
    #         low = threshold
