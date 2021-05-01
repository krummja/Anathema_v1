from __future__ import annotations
from typing import *
import numpy as np
import tcod
import time

from random import randint
from world_engine.data_classes import *
from world_engine.utilities import *


def generate_world():
    print(" ** World Gen START ** ")
    start_time = time.time()

    heightmap = tcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(250):
        tcod.heightmap_add_hill(
            heightmap,
            randint(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10),
            randint(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10),
            randint(12, 16), randint(6, 10)
        )
    print(" -- Main Hills -- ")

    for i in range(1000):
        tcod.heightmap_add_hill(
            heightmap,
            randint(WORLD_WIDTH / 10, WORLD_WIDTH - WORLD_WIDTH / 10),
            randint(WORLD_HEIGHT / 10, WORLD_HEIGHT - WORLD_HEIGHT / 10),
            randint(2, 4), randint(6, 10)
        )
    print(" -- Small Hills -- ")

    tcod.heightmap_normalize(heightmap, 0.0, 1.0)

    noise_hm = tcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    noise2D = tcod.noise_new(2, tcod.NOISE_DEFAULT_HURST, tcod.NOISE_DEFAULT_LACUNARITY)
    tcod.heightmap_add_fbm(noise_hm, noise2D, 6, 6, 0, 0, 32, 1, 1)
    tcod.heightmap_normalize(noise_hm, 0.0, 1.0)
    tcod.heightmap_multiply_hm(heightmap, noise_hm, heightmap)
    print(" -- Apply Simplex -- ")

    pole_generator(heightmap, 0)
    print(" -- South Pole -- ")

    pole_generator(heightmap, 1)
    print(" -- North Pole -- ")

    tectonic_gen(heightmap, 0)
    tectonic_gen(heightmap, 1)
    print(" -- Tectonics -- ")

    tcod.heightmap_rain_erosion(heightmap, WORLD_WIDTH * WORLD_HEIGHT, 0.07, 0)
    print(" -- Erosion -- ")

    tcod.heightmap_clamp(heightmap, 0.0, 1.0)
    # _temperature = tcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    # heightmap, _temperature = temperature(_temperature, heightmap)
    # tcod.heightmap_normalize(_temperature, 0.0, 1.0)
    # print(" -- Temperature -- ")
    #
    # _precipitation = tcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    # _precipitation, _temperature = precipitation(_precipitation, _temperature)
    # tcod.heightmap_normalize(_precipitation, 0.0, 1.0)
    # print(" -- Precipitation -- ")
    #
    # _drainage = tcod.heightmap_new(WORLD_WIDTH, WORLD_HEIGHT)
    # drain_noise = tcod.noise_new(2, tcod.NOISE_DEFAULT_HURST, tcod.NOISE_DEFAULT_LACUNARITY)
    # tcod.heightmap_add_fbm(_drainage, drain_noise, 2, 2, 0, 0, 32, 1, 1)
    # tcod.heightmap_normalize(_drainage, 0.0, 1.0)
    # print(" -- Drainage -- ")

    print(" ** World Gen DONE ** ")

    elapsed_time = time.time() - start_time
    print(f"   elapsed time: {elapsed_time} ")

    print(" -- Initializing Tiles -- ")
    world = [[0 for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)]

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            # print(tcod.heightmap_get_value(heightmap, x, y))
            world[x][y] = Tile(
                tcod.heightmap_get_value(heightmap, x, y), 0, 0, 0, 0
            )

    prosperity(world)
    print(" -- Prosperity -- ")

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            if 0.10 <= world[x][y].precip < 0.33 and world[x][y].drain < 0.5:
                world[x][y].biome_id = 3
                if randint(1, 2) == 2:
                    world[x][y].biome_id = 16

            if world[x][y].precip >= 0.10 and world[x][y].precip > 0.33:
                world[x][y].biome_id = 2
                if world[x][y].precip >= 0.66:
                    world[x][y].biome_id = 1

            if 0.33 <= world[x][y].precip < 0.66 and world[x][y].drain >= 0.33:
                world[x][y].biome_id = 15
                if randint(1, 5) == 5:
                    world[x][y].biome_id = 5

            if world[x][y].temp > 0.2 and world[x][y].precip >= 0.66 and world[x][y].drain > 0.33:
                world[x][y].biome_id = 5
                if world[x][y].precip >= 0.75:
                    world[x][y].biome_id = 6
                if randint(1, 5) == 5:
                    world[x][y].biome_id = 15

            if 0.10 <= world[x][y].precip < 0.33 and world[x][y].drain >= 0.5:
                world[x][y].biome_id = 16
                if randint(1, 2) == 2:
                    world[x][y].biome_id = 14

            if world[x][y].precip < 0.10:
                world[x][y].biome_id = 4
                if world[x][y].drain > 0.5:
                    world[x][y].biome_id = 16
                    if randint(1, 2) == 2:
                        world[x][y].biome_id = 14

                if world[x][y].drain >= 0.66:
                    world[x][y].biome_id = 8

            if world[x][y].height <= 0.2:
                world[x][y].biome_id = 0

            if world[x][y].temp <= 0.2 and world[x][y].height > 0.15:
                world[x][y].biome_id = randint(11, 13)

            if world[x][y].height > 0.6:
                world[x][y].biome_id = 9
            if world[x][y].height > 0.9:
                world[x][y].biome_id = 10

    print(" -- Biome IDs Allocated -- ")

    river_gen(world)
    print(" -- Rivers Carved -- ")

    tcod.heightmap_delete(heightmap)
    # tcod.heightmap_delete(_temperature)
    # tcod.heightmap_delete(noise_hm)

    print(" -- Reticulating Splines -- ")
    return world


def terrain_map(console, world):
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            hm_v = world[x][y].height
            tcod.console_put_char_ex(
                console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '0',
                tcod.blue, tcod.black
            )
            if hm_v > 0.1:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '1',
                    tcod.blue, tcod.black
                )
            if hm_v > 0.2:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '2',
                    palette[0], tcod.black
                )
            if hm_v > 0.3:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '3',
                    palette[1], tcod.black
                )
            if hm_v > 0.4:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '4',
                    palette[2], tcod.black
                )
            if hm_v > 0.5:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '5',
                    palette[3], tcod.black
                )
            if hm_v > 0.6:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '6',
                    palette[4], tcod.black
                )
            if hm_v > 0.7:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '7',
                    palette[5], tcod.black
                )
            if hm_v > 0.8:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '8',
                    tcod.dark_sepia, tcod.black
                )
            if hm_v > 0.9:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '9',
                    tcod.light_gray, tcod.black
                )
            if hm_v > 0.99:
                tcod.console_put_char_ex(
                    console, x, y + CONSOLE_HEIGHT//2 - WORLD_HEIGHT//2, '^',
                    tcod.lighter_gray, tcod.black
                )
    tcod.console_flush()
    return


palette = [
    tcod.Color(25, 255, 25),
    tcod.Color(25, 200, 25),
    tcod.Color(25, 150, 25),
    tcod.Color(25, 100, 25),
    tcod.Color(25, 50, 25),
    tcod.Color(25, 25, 25),
]


def normal_map(world):
    characters = [[0 for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)]
    colors = [[0 for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)]

    def symbol_lookup(x):
        char = None
        if x == 15 or x == 8:
            char = (251, ",")[randint(1, 2) == 2]
        if x == 1:
            char = (244, 131)[randint(1, 2) == 2]
        if x == 2:
            char = ('"', 163)[randint(1, 2) == 2]
        return {
            0: '\367',
            1: char,
            2: char,
            3: 'n',
            4: '\367',
            5: 24,
            6: 6 - randint(0, 1),
            8: char,
            9: 127,
            10: 30,
            11: 176,
            12: 177,
            13: 178,
            14: 'n',
            15: char,
            16: 139
        }[x]

    def color_lookup(x):
        badlands   = tcod.Color( 204, 159,  81 )
        ice        = tcod.Color( 176, 223, 215 )
        darkgreen  = tcod.Color(  68, 158,  53 )
        lightgreen = tcod.Color( 131, 212,  82 )
        water      = tcod.Color(  13, 103, 196 )
        mountain   = tcod.Color( 185, 192, 162 )
        desert     = tcod.Color( 255, 218,  90 )
        return {
            0: water,
            1: darkgreen,
            2: lightgreen,
            3: lightgreen,
            4: desert,
            5: darkgreen,
            6: darkgreen,
            8: badlands,
            9: mountain,
            10: mountain,
            11: ice,
            12: ice,
            13: ice,
            14: darkgreen,
            15: lightgreen,
            16: darkgreen
        }[x]

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            characters[x][y] = symbol_lookup(world[x][y].biome_id)
            colors[x][y] = color_lookup(world[x][y].biome_id)
            if world[x][y].has_river:
                characters[x][y] = 'o'
                colors[x][y] = tcod.light_blue

    return characters, colors


world = generate_world()
tcod.console_set_custom_font("Andux_cp866ish.png", tcod.FONT_LAYOUT_ASCII_INROW)
console = tcod.console_init_root(
    CONSOLE_WIDTH,
    CONSOLE_HEIGHT,
    'WorldGen',
    False,
    tcod.RENDERER_SDL
)

is_running = False
needs_update = False
chars, colors = normal_map(world)

while not tcod.console_is_window_closed():
    while is_running:
        tcod.console_check_for_keypress(True)
        if tcod.console_is_key_pressed(tcod.KEY_SPACE):
            timer = 0
            is_running = False
            print(" ** PAUSED ** ")
            time.sleep(1)

        if needs_update:
            needs_update = False

    key = tcod.console_wait_for_keypress(True)
    if tcod.console_is_key_pressed(tcod.KEY_SPACE):
        is_running = True
        print(" ** RUNNING ** ")
        time.sleep(1)

    terrain_map(console, world)
