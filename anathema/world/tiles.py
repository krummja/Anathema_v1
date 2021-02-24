from typing import Optional
from anathema.utils.color import Palette, Color
from anathema.world.tile_type import TileType


def tile(name: str, char: str, fore: Color, back: Optional[Color] = None):
    return TileType(name, char, fore, back)


class Tiles:

    # Temporary tiles for stage generation

    unformed = tile("unformed", "?", Palette.light_cool_gray).open()
    unformed_wet = tile("unformed_wet", "≈", Palette.light_blue).open()
    open_ground = tile("open", "·", Palette.light_cool_gray).open()
    solid = tile("solid", "#", Palette.light_cool_gray).solid()
    passage = tile("passage", "-", Palette.light_cool_gray).open()
    solid_wet = tile("solid_wet", "≈", Palette.cool_gray).obstacle()
    passage_wet = tile("passage_wet", "-", Palette.light_blue).open()
    doorway = tile("doorway", "○", Palette.light_cool_gray).open()

    # Real Tiles

    ## Walls
    flagstone_wall = tile("flagstone_wall", "▒", Palette.light_warm_gray, Palette.warm_gray).solid()
    granite_wall = tile("granite_wall", "▒", Palette.cool_gray).solid()
    granite_1 = tile("granite_1", "▓", Palette.dark_cool_gray).solid()

    ## Floors
    flagstone_floor = tile("flagstone_floor", "·", Palette.warm_gray, Palette.dark_warm_gray).open()
    granite_floor = tile("granite_floor", "·", Palette.dark_cool_gray, Palette.darker_cool_gray).open()

    dirt_1 = tile("dirt_1", "·", Palette.brown).open()
    dirt_2 = tile("dirt_2", "φ", Palette.brown).open()
    grass = tile("grass", "░", Palette.lima).open()
    tall_grass = tile("tall_grass", "√", Palette.pea_green).obfuscated()

    tree_1 = tile("tree", "▲", Palette.sherwood).solid()

    shallow_water = tile("shallow_water", "≈", Palette.light_blue).open()

    ## Doorways
    open_door = tile("open_door", "○", Palette.dark_brown).door().closable()
    closed_door = tile("closed_door", "◙", Palette.dark_brown).door().openable()

    # Chests
    open_chest = tile("open_chest", "⌠", Palette.tan).obstacle().container().closable()
    closed_chest = tile("closed_chest", "⌡", Palette.tan).obstacle().container().openable()
