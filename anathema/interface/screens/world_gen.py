from __future__ import annotations
from typing import *
from morphism import *
from math import ceil
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
from anathema.interface.views.text_input import TextInputView, TextInputConfig
from anathema.engine.world.tile import tile_graphic
from anathema.data import *
from anathema.storage import *
from anathema.engine.core.world import WorldData, TestArea

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


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


def option_filter(key, val):
    self.set_option(key, val)


class WorldGen(UIScreen):

    def __init__(self, game: Game):
        self.position = (ceil(Options.WORLD_WIDTH // 2), ceil(Options.WORLD_HEIGHT // 2))
        self.menu_options = {
            'View': ['Standard', 'Biome', 'Rainfall', 'Temp'],
            'Palette': ['Normal', 'Red', 'Knutux'],
        }
        self.configuration = {
            'View': 'Standard',
            'Palette': 'Normal',
        }
        self.lat_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left = 2, top = 2, width = 0.5, right = None)
        )
        self.long_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left = 14, top = 2, width = 0.5, right = None)
        )
        self.height_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left = 2, top = 4, width = 0.5, right = None)
        )
        self.biome_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left = 2, top = 6, width = 0.5, right = None)
        )
        self.temp_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left = 2, top = 8, width = 0.5, right = None)
        )
        self.rainfall_label = LabelView(
            text = "", align_horz = 'left', align_vert = 'top',
            layout = Layout.row_top(0.2).with_updates(left = 18, top = 8, width = 0.5, right = None)
        )
        self.settings_list = SettingsListView(
            label_control_pairs = [
                (k, CyclingButtonView(
                    k, v, v[0], callback=option_filter, align_horz = 'left'))
                for k, v in sorted(self.menu_options.items())
            ],
            value_column_width = 12,
            layout = Layout(left = 2, right = 2, top = 10, bottom = 20),
        )

        views = [
            RectView(
                layout = Layout(left = Options.STAGE_PANEL_WIDTH),
                subviews = [
                    self.lat_label,
                    self.long_label,
                    self.height_label,
                    self.biome_label,
                    self.temp_label,
                    self.rainfall_label,
                    self.settings_list,
                    ButtonView(
                        text = "Apply",
                        callback = self.ui_apply_options,
                        align_horz = 'left',
                        layout = Layout.row_bottom(0.2).with_updates(left = 2, bottom = 7)
                    ),
                    ButtonView(
                        text = "New World",
                        callback = self.ui_generate_new,
                        align_horz = 'left',
                        layout = Layout.row_bottom(0.2).with_updates(left = 2, bottom = 5)
                    ),
                    ButtonView(
                        text = "Continue",
                        callback = self.ui_continue,
                        align_horz = 'left',
                        layout = Layout.row_bottom(0.2).with_updates(left = 2, bottom = 3)
                    ),
                    ButtonView(
                        text = "Back",
                        callback = self.ui_back,
                        align_horz = 'left',
                        layout = Layout.row_bottom(0.2).with_updates(left = 2, bottom = 1)
                    )
                ]
            )
        ]
        super().__init__(name="WORLD GEN", game=game, views=views)
        self.covers_screen = True

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def on_enter(self):
        Options.STAGE_PANEL_HEIGHT = Options.CONSOLE_HEIGHT
        self.generate()
        self.game.camera.camera_pos = self.position

    def cmd_escape(self):
        pass

    def pre_update(self):
        self.game.render_system.draw_world_map()
        cam_x, cam_y = self.game.camera.camera_pos
        x = self.position[0] - cam_x
        y = self.position[1] - cam_y
        self.game.console.root.tiles_rgb[["fg", "bg"]][y][x] = (0, 0, 0), (255, 0, 0)

    def post_update(self):
        world_data = self.game.world.planet_view.world_data
        self.lat_label.update(self.tile_to_coord(0, self.y))
        self.long_label.update(self.tile_to_coord(1, self.x))
        self.height_label.update(
            "Height: " + str(round(world_data[self.y][self.x]['height'], 2)))
        self.biome_label.update(
            "Biome:  " + self.biome_name(world_data[self.y][self.x]["biome_id"]))
        self.temp_label.update(
            "Temp:   " + str(round(world_data[self.y][self.x]["temperature"], 2)))
        self.rainfall_label.update(
            "Rain:   " + str(round(world_data[self.y][self.x]["precipitation"], 2)))

    def move_focus(self, direction):
        WIDTH = self.game.world.generator.width
        HEIGHT = self.game.world.generator.height
        target_x = self.x + direction[0]
        target_y = self.y + direction[1]
        if 0 <= target_x < WIDTH and 0 <= target_y < HEIGHT:
            self.position = (target_x, target_y)
            self.game.camera.camera_pos = self.position

    def set_option(self, key, value):
        self.configuration[key] = value

    def ui_apply_options(self):
        self.get_current_view()
        self.game.console.root.clear()

    def ui_generate_new(self):
        self.generate()

    def ui_continue(self):
        self.game.screens.push_screen(FinalizeWorld(self.game, self.position))

    def ui_back(self):
        self.game.screens.replace_screen(self.game.screens.screens["MAIN MENU"])

    def generate(self):
        self.game.world.generator.generate()
        self.game.world.planet_view.generate_standard_view(
            RENDER_CONFIGURATION['Palette'][self.configuration['Palette']]
        )
        self.game.console.root.clear()

    def get_current_view(self):
        if self.configuration['View'] == 'Standard':
            self.game.world.planet_view.generate_standard_view(
                RENDER_CONFIGURATION['Palette'][self.configuration['Palette']]
            )
        if self.configuration['View'] == 'Biome':
            self.game.world.planet_view.generate_biome_view()
        if self.configuration['View'] == 'Rainfall':
            self.game.world.planet_view.generate_precipitation_view()
        if self.configuration['View'] == 'Temp':
            self.game.world.planet_view.generate_temperature_view()

    @staticmethod
    def tile_to_coord(lat_long: int, tile: int) -> str:
        suf = (("N", "S"), ("W", "E"))[lat_long]
        coord = (tile * 360) / (Options.WORLD_HEIGHT, Options.WORLD_WIDTH)[lat_long]
        if coord < 180:
            return "{:4}".format(str(int(180 - coord))) + suf[0]
        if coord > 180:
            return "{:4}".format(str(int(coord - 180))) + suf[1]
        return ("- EQUATOR -", "- MERIDIAN -")[lat_long]

    @staticmethod
    def biome_name(biome_id: int) -> str:
        return {
            0: "ice cap",
            1: "tundra",
            2: "subarctic",
            3: "dry steppe",
            4: "dry desert",
            5: "highland",
            6: "humid continental",
            7: "dry summer subtropic",
            8: "tropical wet & dry",
            9: "marine west coast",
            10: "humid subtropical",
            11: "wet tropics",
            12: "ocean",
            13: "shallow ocean"
        }[biome_id]


class FinalizeWorld(UIScreen):

    def __init__(self, game: Game, position: Tuple[int, int]) -> None:
        self.world_id: str = ""
        self.position = position
        self.input = TextInputView(
            config = TextInputConfig(),
            callback = self.ui_set_world_id,
            layout = Layout(top = 1, left = 1)
        )
        super().__init__(name = "FINALIZE WORLD", game = game, views = [
            RectView(
                layout = Layout.centered(20, 8),
                subviews = [
                    self.input,
                    ButtonView(
                        "Back", callback = self.ui_back,
                        align_vert = "top", align_horz = "left",
                        layout = Layout.row_bottom(1).with_updates(bottom = 1, left = 1)
                    ),
                    ButtonView(
                        "Done", callback = self.ui_confirm,
                        align_vert = "top", align_horz = "right",
                        layout = Layout.row_bottom(1).with_updates(right = 1, bottom = 1)
                    )
                ]
            )
        ])

    def on_enter(self, *args):
        self.view.find_prev_responder()

    def ui_set_world_id(self, value):
        self.world_id = value

    def ui_back(self):
        self.game.screens.pop_screen()

    def ui_confirm(self):
        world_data = WorldData(self.world_id)
        world_data.new_area(self.position, TestArea())
        world_save = WorldSave(
            world_id = world_data.world_id,
            buildable = world_data.buildable,
            area_registry = world_data.area_registry
        )
        Storage.new_game_setup(self.game.session, world_save)
        self.game.screens.replace_screen(self.game.screens.screens["MAIN MENU"])
