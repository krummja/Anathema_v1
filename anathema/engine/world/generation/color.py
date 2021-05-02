from tcod import color
import numpy as np
from anathema.engine.world.tile import tile_graphic


class Color:
    black = (0x00, 0x00, 0x00)
    white = (0xFF, 0xFF, 0xFF)
    nero = (0x15, 0x15, 0x15)
    light_cool_gray = (0x74, 0x92, 0xb5)
    cool_gray = (0x3f, 0x4b, 0x73)
    dark_cool_gray = (0x26, 0x2a, 0x42)
    darker_cool_gray = (0x14, 0x13, 0x1f)

    light_warm_gray = (0x84, 0x7e, 0x87)
    warm_gray = (0x48, 0x40, 0x4a)
    dark_warm_gray = (0x2a, 0x24, 0x2b)
    darker_warm_gray = (0x16, 0x11, 0x17)

    sandal = (0xbd, 0x90, 0x6c)
    tan = (0x8e, 0x52, 0x37)
    brown = (0x99, 0x6a, 0x56)
    dark_brown = (0x5c, 0x47, 0x3e)

    light_blue = (0x40, 0xa3, 0xe5)
    blue = (0x15, 0x57, 0xc2)
    dark_blue = (0x1a, 0x2e, 0x96)

    mint = (0x81, 0xd9, 0x75)
    lima = (0x83, 0x9e, 0x0d)
    pea_green = (0x16, 0x75, 0x26)
    sherwood = (0x00, 0x40, 0x27)


test_palette = np.array(
            [
                (ord("≈"), color.Color( 20,  40, 130), color.Color(21, 21, 21)),
                (ord("≈"), color.Color( 20,  60, 165), color.Color(21, 21, 21)),
                (ord("≈"), color.Color( 60, 100, 210), color.Color(21, 21, 21)),
                (ord("2"), color.Color(175, 215, 170), color.Color(21, 21, 21)),
                (ord("3"), color.Color(125, 200, 140), color.Color(21, 21, 21)),
                (ord("4"), color.Color(100, 175, 100), color.Color(21, 21, 21)),
                (ord("5"), color.Color(100, 135,  95), color.Color(21, 21, 21)),
                (ord("6"), color.Color( 60, 110,  55), color.Color(21, 21, 21)),
                (ord("7"), color.Color( 30,  90,  25), color.Color(21, 21, 21)),
                (ord("8"), color.Color( 60,  65,  60), color.Color(21, 21, 21)),
                (ord("▲"), color.Color(160, 160, 160) - color.Color(40, 40, 40), color.Color(21, 21, 21)),
                (ord("▲"), color.Color(190, 190, 190), color.Color(21, 21, 21)),
            ],
            dtype=tile_graphic
        )
