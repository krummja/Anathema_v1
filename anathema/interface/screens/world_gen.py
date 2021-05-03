from __future__ import annotations
from typing import *
from morphism import *
import numpy as np
import tcod
from tcod import color

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView, CyclingButtonView
from anathema.interface.views.collection_list import SettingsListView
from anathema.engine.world.tile import tile_graphic

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


Options.STAGE_PANEL_HEIGHT = Options.CONSOLE_HEIGHT

RENDER_CONFIGURATION = {
    'Palette': {
        'Normal': np.array([
            (ord("≈"), color.Color( 20,  40, 130), color.Color(21, 21, 21)),
            (ord("≈"), color.Color( 20,  60, 165), color.Color(21, 21, 21)),
            (ord("≈"), color.Color( 60, 100, 210), color.Color(21, 21, 21)),
            (ord("2"), color.Color(175, 215, 170), color.Color(21, 21, 21)),
            (ord("3"), color.Color(125, 200, 140), color.Color(21, 21, 21)),
            (ord("4"), color.Color(100, 175, 100), color.Color(21, 21, 21)),
            (ord("5"), color.Color(100, 135,  95), color.Color(21, 21, 21)),
            (ord("6"), color.Color( 60, 110,  55), color.Color(21, 21, 21)),
            (ord("7"), color.Color( 30,  90,  25), color.Color(21, 21, 21)),
            (ord("8"), color.Color( 30,  65,  30), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(120, 120, 120), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(190, 190, 190), color.Color(21, 21, 21)),
        ], dtype = tile_graphic),
        'Red'   : np.array([
            (ord("≈"), color.Color( 35, 0, 0), color.Color(21, 21, 21)),
            (ord("≈"), color.Color( 66, 0, 0), color.Color(21, 21, 21)),
            (ord("≈"), color.Color( 90, 0, 0), color.Color(21, 21, 21)),
            (ord("2"), color.Color(110, 0, 0), color.Color(21, 21, 21)),
            (ord("3"), color.Color(130, 0, 0), color.Color(21, 21, 21)),
            (ord("4"), color.Color(150, 0, 0), color.Color(21, 21, 21)),
            (ord("5"), color.Color(170, 0, 0), color.Color(21, 21, 21)),
            (ord("6"), color.Color(190, 0, 0), color.Color(21, 21, 21)),
            (ord("7"), color.Color(210, 0, 0), color.Color(21, 21, 21)),
            (ord("8"), color.Color(235, 0, 0), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(245, 0, 0), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(255, 0, 0), color.Color(21, 21, 21)),
        ], dtype = tile_graphic),
        'Knutux': np.array([
            (ord("≈"), color.Color(  20,   40,  130), color.Color(21, 21, 21)),
            (ord("≈"), color.Color(  20,   60,  165), color.Color(21, 21, 21)),
            (ord("≈"), color.Color(  80,  125,  230), color.Color(21, 21, 21)),
            (ord("2"), color.Color(0x4a, 0xad, 0x5a), color.Color(21, 21, 21)),
            (ord("3"), color.Color(0x74, 0xc3, 0x53), color.Color(21, 21, 21)),
            (ord("4"), color.Color(0xb5, 0xd6, 0x63), color.Color(21, 21, 21)),
            (ord("5"), color.Color(0xde, 0xde, 0x63), color.Color(21, 21, 21)),
            (ord("6"), color.Color(0xff, 0xe7, 0x10), color.Color(21, 21, 21)),
            (ord("7"), color.Color(0xff, 0xce, 0x08), color.Color(21, 21, 21)),
            (ord("8"), color.Color(0xff, 0x9c, 0x08), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(0xff, 0xee, 0xbd), color.Color(21, 21, 21)),
            (ord("▲"), color.Color(0xff, 0xfe, 0xfc), color.Color(21, 21, 21)),
        ], dtype = tile_graphic),
    }
}

MENU_OPTIONS = {
    'View': ['Standard', 'Biome'],
    'Palette': ['Normal', 'Red', 'Knutux']
}


class WorldGen(UIScreen):

    def __init__(self, game: Game):
        self.position = (0, 0)
        self.configuration = {
            'View': 'Standard',
            'Palette': 'Normal'
        }

        self.lat_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left=2, top=2, width=0.5, right=None)
            )
        self.long_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left=10, top=2, width=0.5, right=None)
            )

        views = [
            RectView(
                layout = Layout(left = Options.STAGE_PANEL_WIDTH),
                subviews = [
                    self.lat_label,
                    self.long_label,
                    SettingsListView(
                        label_control_pairs = [
                            (label, CyclingButtonView(
                                options = value,
                                initial_value = value[0],
                                callback = (lambda val: self.set_option(label, val)),
                                align_horz = 'left'))
                            for label, value in sorted(MENU_OPTIONS.items())
                        ],
                        value_column_width = 12,
                        layout = Layout(left = 2, right = 2, top = 10, bottom = 20),
                    ),
                    ButtonView(
                        text = "Apply",
                        callback = self.apply_options,
                        align_horz = 'left',
                        layout = Layout.row_bottom(0.2).with_updates(left = 2, bottom = 3)
                    ),
                    ButtonView(
                        text = "New World",
                        callback = self.generate_new,
                        align_horz = 'left',
                        layout = Layout.row_bottom(0.2).with_updates(left = 2, bottom = 1)
                    ),
                ]
            )
        ]
        super().__init__(name="WORLD GEN", game=game, views=views)
        self.covers_screen = True

    def on_enter(self):
        self.generate_new()

    def cmd_escape(self):
        self.game.screens.pop_screen()

    def pre_update(self):
        self.game.render_system.draw_world_map()
        cam_x, cam_y = self.game.camera.camera_pos
        x = self.position[0] - cam_x
        y = self.position[1] - cam_y
        self.game.console.root.tiles_rgb[["fg", "bg"]][y][x] = (0, 0, 0), (255, 0, 0)

    def post_update(self):
        self.lat_label.update(tile_to_coord(0, 160, self.position[1]))
        self.long_label.update(tile_to_coord(1, 240, self.position[0]))

    def move_focus(self, direction):
        WIDTH = self.game.world.generator.width
        HEIGHT = self.game.world.generator.height
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]
        if 0 <= target_x < WIDTH and 0 <= target_y < HEIGHT:
            self.position = (target_x, target_y)
            self.game.camera.camera_pos = self.position

    def set_option(self, key, value):
        self.configuration[key] = value

    def generate_new(self):
        self.game.world.generator.generate()
        self.game.world.planet_view.generate_standard_view(
            RENDER_CONFIGURATION['Palette'][self.configuration['Palette']]
        )
        self.game.console.root.clear()

    def apply_options(self):
        if self.configuration['View'] == 'Standard':
            self.game.world.planet_view.generate_standard_view(
                RENDER_CONFIGURATION['Palette'][self.configuration['Palette']]
            )
        if self.configuration['View'] == 'Biome':
            self.game.world.planet_view.generate_biome_view()
        self.game.console.root.clear()


def tile_to_coord(lat_long: int, max_val: int, tile: int) -> str:
    suf = (("N", "S"), ("W", "E"))[lat_long]
    coord = (tile * 360) / max_val
    if coord < 180:
        return "{:4}".format(str(int(180 - coord))) + suf[0]
    if coord > 180:
        return "{:4}".format(str(int(coord - 180))) + suf[1]
    return ("- EQUATOR -", "- MERIDIAN -")[lat_long]
