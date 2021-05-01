from __future__ import annotations
from typing import *
from random import *

import tcod
from .data_classes import *


def point_distance_round(x1: int, y1: int, x2: int, y2: int) -> int:
    return round( abs(x2 - x1) + abs(y2 - y1) )


def lowest_neighbor(world, x: int, y: int):
    min_val: int = 1
    _x: int = 0
    _y: int = 0

    if world[x + 1][y].height < min_val and x + 1 < WORLD_WIDTH:
        min_val = world[x + 1][y].height
        _x, _y = x + 1, y

    if world[x][y + 1].height < min_val and y + 1 < WORLD_HEIGHT:
        min_val = world[x][y + 1].height
        _x, _y = x, y + 1

    if world[x - 1][y].height < min_val and x - 1 > 0:
        min_val = world[x - 1][y].height
        _x, _y = x - 1, y

    if world[x][y - 1].height < min_val and y - 1 > 0:
        min_val = world[x][y - 1].height
        _x, _y = x, y - 1

    error = 0
    if x == 0 and y == 0:
        error = 1
    return _x, _y, error


def pole_generator(heightmap, ns: int):

    if ns == 0:
        rng = randint(2, 5)
        for i in range(WORLD_WIDTH):
            for j in range(rng):
                tcod.heightmap_set_value(heightmap, i, WORLD_HEIGHT - 1 - j, 0.31)
            rng += randint(1, 3) - 2
            rng = min(max(2, rng), 5)

    if ns == 1:
        rng = randint(2, 5)
        for i in range(WORLD_WIDTH):
            for j in range(rng):
                tcod.heightmap_set_value(heightmap, i, j, 0.31)
            rng += randint(1, 3) - 2
            rng = min(max(2, rng), 5)


def tectonic_gen(heightmap, hor):
    tectonic_tiles = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
    if hor == 1:
        pos = randint(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10)
        for x in range(WORLD_WIDTH):
            tectonic_tiles[x][pos] = 1
            pos += randint(1, 5) - 3
            pos = min(max(0, pos), WORLD_HEIGHT - 1)

    if hor == 0:
        pos = randint(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10)
        for y in range(WORLD_HEIGHT):
            tectonic_tiles[pos][y] = 1
            pos += randint(1, 5) - 3
            pos = min(max(0, pos), WORLD_WIDTH - 1)

    for x in range(WORLD_WIDTH // 10, WORLD_WIDTH - WORLD_WIDTH // 10):
        for y in range(WORLD_HEIGHT // 10, WORLD_HEIGHT - WORLD_HEIGHT // 10):
            if tectonic_tiles[x][y] == 1 and tcod.heightmap_get_value(heightmap, x, y) > 0.3:
                tcod.heightmap_add_hill(heightmap, x, y, randint(2, 4), uniform(0.15, 0.18))

    return heightmap


def temperature(heightmap, temp):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            height_effect = 0
            if y > WORLD_HEIGHT / 2:
                tcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT - y - height_effect)
            else:
                tcod.heightmap_set_value(temp, x, y, y - height_effect)
            height_effect = tcod.heightmap_get_value(heightmap, x, y)

            if height_effect > 0.8:
                height_effect *= 5
                if y > WORLD_HEIGHT / 2:
                    tcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT - y - height_effect)
                else:
                    tcod.heightmap_set_value(temp, x, y, y - height_effect)

            if height_effect < 0.25:
                height_effect *= 10
                if y > WORLD_HEIGHT / 2:
                    tcod.heightmap_set_value(temp, x, y, WORLD_HEIGHT - y - height_effect)
                else:
                    tcod.heightmap_set_value(temp, x, y, y - height_effect)

    return heightmap, temp


def precipitation(precip_heightmap, temp_heightmap):
    precip_heightmap[:] += 2
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            temp = tcod.heightmap_get_value(temp_heightmap, x, y)
    precipitation = tcod.noise_new(2, tcod.NOISE_DEFAULT_HURST, tcod.NOISE_DEFAULT_LACUNARITY)
    tcod.heightmap_add_fbm(precip_heightmap, precipitation, 2, 2, 0, 0, 32, 1, 1)
    tcod.heightmap_normalize(precip_heightmap, 0.0, 1.0)

    return precip_heightmap, temp_heightmap


def river_gen(world):
    x = randint(0, WORLD_WIDTH - 1)
    y = randint(0, WORLD_HEIGHT - 1)
    _x = []
    _y = []
    tries = 0

    while world[x][y].height < 0.8:
        tries += 1
        x = randint(0, WORLD_WIDTH - 1)
        y = randint(0, WORLD_HEIGHT - 1)
        if tries > 2000:
            return

    del _x[:]
    del _y[:]

    _x.append(x)
    _y.append(y)

    while world[x][y].height >= 0.2:
        x, y, error = lowest_neighbor(world, x, y)
        if error == 1:
            return
        try:
            if (
                world[x][y].has_river or
                world[x+1][y].has_river or
                world[x-1][y].has_river or
                world[x][y+1].has_river or
                world[x][y-1].has_river
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
        if world[_x[i]][_y[i]].height < 0.2:
            break
        world[_x[i]][_y[i]].has_river = True
        if world[_x[i]][_y[i]].height >= 0.2 and i == len(_x):
            world[_x[i]][_y[i]].has_river = True


def prosperity(world):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            world[x][y].prosperity = (
                1.0 - abs(world[x][y].precip - 0.6)
                + 1.0 - abs(world[x][y].temp - 0.5)
                + world[x][y].drain) / 3
