from __future__ import annotations
from typing import *
from random import randint, uniform
import numpy as np
import tcod
from tcod.color import Color
from anathema.engine.world.planet.heightmap import *
from anathema.engine.world.tile import tile_graphic
from anathema.engine.core.options import Options

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

    def __init__(self, height: int, width: int) -> None:
        """
        height      world map height in tiles
        width       world map width in tiles
        """
        self.height = height
        self.width = width
        self.heightmap = Heightmap(height, width)
        self.world_data = np.zeros((height, width), world_tile, order="C")
        self.messages = []

    def generate(self):
        print("Initializing")
        self.initialize_map()
        print("Generating Polar Regions...")
        self.pole_generator(0)
        self.pole_generator(1)
        print("Tectonic Simulation: Pass 1")
        self.tectonic_generator(0)
        print("Tectonic Simulation: Pass 2")
        self.tectonic_generator(1)
        print("Simulating Rain Erosion")
        self.heightmap.rain_erode()
        print("Initializing World Data...")
        self.initialize_world_data()
        print("Done!")
        # self.river_gen()

    def initialize_map(self):
        self.heightmap.add_mountains(250)
        self.heightmap.add_hills(1000)
        self.heightmap.normalize()
        self.heightmap.apply_simplex_noise()

    def initialize_world_data(self):
        self.world_data["height"][:] = self.heightmap._array[:]
        self.temperature()
        self.precipitation()
        self.drainage()

        temp_factor = self.height / 2
        for x in range(self.width):
            for y in range(self.height):

                # Ice Cap, Tundra, Subarctic, Highland
                if (self.world_data[y][x]["precipitation"] < 0.5
                        and self.world_data[y][x]["temperature"] < 0.08 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 0   # ice cap

                if (self.world_data[y][x]["precipitation"] < 0.5
                        and 0.08 * temp_factor <= self.world_data[y][x]["temperature"] < 0.15 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 1   # tundra

                if (self.world_data[y][x]["precipitation"] < 0.5
                        and 0.15 * temp_factor <= self.world_data[y][x]["temperature"] < 0.23 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 2   # subarctic

                if (0.5 <= self.world_data[y][x]["precipitation"]
                        and self.world_data[y][x]["temperature"] < 0.23 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 5   # highland

                # Dry Steppe, Dry Desert
                if (self.world_data[y][x]["precipitation"] < 0.32
                        and 0.23 * temp_factor <= self.world_data[y][x]["temperature"] < 0.54 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 3   # dry steppe

                if (self.world_data[y][x]["precipitation"] < 0.32
                        and 0.54 * temp_factor <= self.world_data[y][x]["temperature"]):
                    self.world_data[y][x]["biome_id"] = 4   # dry desert

                # Humid Continental, Dry Summer Subtropics, Tropical Wet & Dry
                if (0.32 <= self.world_data[y][x]["precipitation"] < 0.82
                        and 0.23 * temp_factor <= self.world_data[y][x]["temperature"] < 0.54 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 6   # humid continental

                if (0.32 <= self.world_data[y][x]["precipitation"] < 0.77
                        and 0.54 * temp_factor <= self.world_data[y][x]["temperature"] < 0.77 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 7   # dry summer subtropic

                if (0.32 <= self.world_data[y][x]["precipitation"] < 0.68
                        and 0.77 * temp_factor <= self.world_data[y][x]["temperature"]):
                    self.world_data[y][x]["biome_id"] = 8   # tropical wet & dry

                # Marine West Coast, Humid Subtropical, Wet Tropics
                if (0.82 <= self.world_data[y][x]["precipitation"]
                        and 0.23 * temp_factor <= self.world_data[y][x]["temperature"] < 0.54 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 9   # marine west coast

                if (0.77 <= self.world_data[y][x]["precipitation"]
                        and 0.54 * temp_factor <= self.world_data[y][x]["temperature"] < 0.77 * temp_factor):
                    self.world_data[y][x]["biome_id"] = 10  # humid subtropical

                if (0.68 <= self.world_data[y][x]["precipitation"]
                        and 0.77 * temp_factor <= self.world_data[y][x]["temperature"]):
                    self.world_data[y][x]["biome_id"] = 11  # wet tropics

                if self.world_data[y][x]["height"] <= 0.3:
                    self.world_data[y][x]["biome_id"] = 12  # ocean

                if 0.2 < self.world_data[y][x]["height"] <= 0.3:
                    self.world_data[y][x]["biome_id"] = 13  # shallow ocean

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
                    self.world_data[y][x]["temperature"] = self.height - y - height_effect
                else:
                    self.world_data[y][x]["temperature"] = y - height_effect
                height_effect = self.heightmap._array[y][x]

                if height_effect > 0.8:
                    height_effect *= 5
                    if y > self.height / 2:
                        self.world_data[y][x]["temperature"] = self.height - y - height_effect
                    else:
                        self.world_data[y][x]["temperature"] = y - height_effect

                if height_effect < 0.25:
                    height_effect *= 10
                    if y > self.height / 2:
                        self.world_data[y][x]["temperature"] = self.height - y - height_effect
                    else:
                        self.world_data[y][x]["temperature"] = y - height_effect

    def precipitation(self):
        precipitation_hm = heightmap_new(self.width, self.height, order="C")
        precipitation_hm[:] += 2
        precipitation_noise = tcod.noise_new(2, tcod.NOISE_DEFAULT_HURST, tcod.NOISE_DEFAULT_LACUNARITY)
        heightmap_add_fbm(precipitation_hm, precipitation_noise, 2, 2, 0, 0, 32, 1, 1)
        heightmap_normalize(precipitation_hm, 0.0, 1.0)
        self.world_data["precipitation"] = precipitation_hm

    def drainage(self):
        drainage_hm = heightmap_new(self.width, self.height, order="C")
        drainage_hm[:] += 2
        drainage_noise = tcod.noise_new(2, tcod.NOISE_DEFAULT_HURST, tcod.NOISE_DEFAULT_LACUNARITY)
        heightmap_add_fbm(drainage_hm, drainage_noise, 2, 2, 0, 0, 32, 1, 1)
        heightmap_normalize(drainage_hm, 0.0, 1.0)
        self.world_data["drainage"] = drainage_hm

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


class PlanetView:

    def __init__(self, generator: PlanetGenerator) -> None:
        self.generator = generator
        self.world_data = generator.world_data
        self.view = np.zeros((self.height, self.width), tile_graphic, order="C")

    @property
    def width(self):
        return self.generator.width

    @property
    def height(self):
        return self.generator.height

    def generate_standard_view(self, palette):
        height = (self.world_data["height"] * 10).clip(0, len(palette) - 1).astype(np.int8)
        self.view[:] = palette[height]

    def generate_temperature_view(self):
        def color_lookup(x):
            return {
                0 : tcod.Color(0, 255, 204),
                1 : tcod.Color(23, 232, 185),
                2 : tcod.Color(46, 209, 167),
                3 : tcod.Color(70, 185, 148),
                4 : tcod.Color(93, 162, 130),
                5 : tcod.Color(116, 139, 111),
                6 : tcod.Color(139, 116, 93),
                7 : tcod.Color(162, 93, 74),
                8 : tcod.Color(185, 70, 56),
                9 : tcod.Color(209, 46, 37),
                10: tcod.Color(232, 23, 19),
                11: tcod.Color(255, 0, 0),
            }[x]

        temperature = self.world_data["temperature"]
        height = self.world_data["height"]
        max_temp = 1
        for x in range(self.width):
            for y in range(self.height):
                temp = temperature[y][x]
                if temp > max_temp:
                    max_temp = temp

                if height[y][x] > 0.3:
                    temp = (temperature[y][x] * 10) / max_temp
                    color = color_lookup(int(temp))
                    self.view[y][x] = (ord("T"), color, (21, 21, 21))

    def generate_precipitation_view(self):
        def color_lookup(x):
            return {
                0 : tcod.Color(255, 0, 0),
                1 : tcod.Color(232, 23, 0),
                2 : tcod.Color(209, 46, 0),
                3 : tcod.Color(185, 70, 0),
                4 : tcod.Color(162, 93, 0),
                5 : tcod.Color(139, 116, 0),
                6 : tcod.Color(116, 139, 0),
                7 : tcod.Color(93, 162, 0),
                8 : tcod.Color(70, 185, 0),
                9 : tcod.Color(46, 209, 0),
                10: tcod.Color(23, 232, 0),
                11: tcod.Color(0, 255, 0),
            }[x]

        precipitation = self.world_data["precipitation"]
        height = self.world_data["height"]
        for x in range(self.width):
            for y in range(self.height):
                if height[y][x] > 0.3:
                    color = color_lookup(ceil(precipitation[y][x] * 10))
                    self.view[y][x] = (ord("P"), color, (21, 21, 21))

    def generate_biome_view(self):
        def symbol_lookup(x):
            return {
                0 : "█",     # ice cap
                1 : "_",     # tundra
                2 : "♠",     # subarctic
                3 : "#",     # dry steppe
                4 : "n",     # dry desert
                5 : "▲",     # highland
                6 : "√",     # humid continental
                7 : ":",     # dry summer subtropic
                8 : "t",     # tropical wet & dry
                9 : "•",     # marine west coast
                10: "√",     # humid subtropical
                11: "f",     # wet tropics
                12: "≈",     # ocean
                13: "≈",     # shallow ocean
            }[x]

        def color_lookup(x):
            badlands = tcod.Color(204, 159, 81)
            ice = tcod.Color(176, 223, 215)
            darkgreen = tcod.Color(68, 158, 53)
            lightgreen = tcod.Color(131, 212, 82)
            water = tcod.Color(13, 103, 196)
            mountain = tcod.Color(185, 192, 162)
            desert = tcod.Color(255, 218, 90)
            return {
                0 : ice,            # ice cap
                1 : ice,            # tundra
                2 : ice,            # subarctic
                3 : badlands,       # dry steppe
                4 : desert,         # dry desert
                5 : mountain,       # highland
                6 : lightgreen,     # humid continental
                7 : lightgreen,     # dry summer subtropic
                8 : lightgreen,     # tropical wet & dry
                9 : desert,         # marine west coast
                10: lightgreen,     # humid subtropical
                11: darkgreen,      # wet tropics
                12: water,          # ocean
                13: water,          # shallow ocean
            }[x]

        for x in range(self.width):
            for y in range(self.height):
                biome = self.world_data[y][x]["biome_id"]
                symbol = symbol_lookup(biome)
                self.view[y][x] = (ord(symbol) if not isinstance(symbol, int) else symbol,
                                   color_lookup(biome),
                                   (21, 21, 21))

    @staticmethod
    def tile_to_coord(lat_long: int, tile: int) -> str:
        suf = (("N", "S"), ("W", "E"))[lat_long]
        coord = (tile * 360) / (Options.WORLD_HEIGHT, Options.WORLD_WIDTH)[lat_long]
        if coord < 180:
            return "{:4}".format(str(int(180 - coord))) + suf[0]
        if coord > 180:
            return "{:4}".format(str(int(coord - 180))) + suf[1]
        return ("- EQUATOR -", "- MERIDIAN -")[lat_long]
