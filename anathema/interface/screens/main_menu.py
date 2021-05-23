from __future__ import annotations
from typing import *
import numpy as np
import tcod
from enum import Enum
from collections import OrderedDict

from morphism import *

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView, CyclingButtonView
from anathema.interface.views.collection_list import SettingsListView
from anathema.data import get_data, get_save

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


POSITION_RECT = Rect(Point(0, 0), Size(Options.CONSOLE_WIDTH, Options.CONSOLE_HEIGHT))


class LogoView(View):

    def draw(self):
        logo = [
            "          █                                                                                            ",
            "          █                                                                                            ",
            "          █                                                                                            ",
            "          █                                                                                            ",
            "          █                                                                                            ",
            "          █                                                                                            ",
            "          █                                                                                            ",
            "   █      █                                                                                            ",
            "          █                                                                                            ",
            "     █   ███      ████████                                                                             ",
            "      ██ ███   ██████████████                                                                          ",
            "      ██ █████████████████████                                                                         ",
            "        ████████████████████████                                     ██    ██                          ",
            "     ██████████████        ██████                                    ██    ██                          ",
            "████████████████              ████              ████  █ ███   ████  ██████ █████   ████  █ █ █   ████  ",
            "     ██████████                ███                 ██ ██  ██     ██  ██    ██  ██ ██  ██ ██ █ █     ██ ",
            "       ██████                    ██             █████ ██  ██  █████  ██    ██  ██ ██████ ██ █ █  █████ ",
            "       █████                      ██           ██  ██ ██  ██ ██  ██  ██    ██  ██ ██     ██ █ █ ██  ██ ",
            "       █████                █      ██           █████ ██  ██  █████   ████ ██  ██  ████  ██ █ █  █████ ",
            "       █████                ██     ██                                                                  ",
            "       ████                █ █      █                                                                  ",
            "      ████                 ████      █                                                                 ",
            "      ████                ██ █ █     █                                                                 ",
            "      ████                █  █  █    █                                                                 ",
            "      ███                 █ ██   █                                                                     ",
            "      ███                █ █  █   █                                                                    ",
            "      ███                ██   ██   █                                                                   ",
            "      ███                █   █  █   ██                                                                 ",
            "      ███               █   █   ██    █                                                                ",
            "       ██           █   █  █   █  █    ██                                                              ",
            "       ██          █ ███  █   █   ██     ██   ██                                                       ",
            "       ███         ██  █ █   █   █ █       ███  █                                                      ",
            "        ██        █ ██  █   █   █  █          █  █                                                     ",
            "         █        ██ █   ███   █   █          █ █ ██                                                   ",
            "         ██      ██  ██    █  █   ██           █   ██                                                  ",
            "          ██     █  █ █     ██   █ █            █ █  ██                                                ",
            "           █     █ █  ██     ██ █   █            █    ███                                              ",
            "            █   █ █  █  ██     █   █ █            ██ █   ██                                            ",
            "               █ █  █  █  █     █ █   ██            █   █  ██                                          ",
            "           ██████  █  █  █ ███████   █  █████████████  █  █ ██████████████                             ",
        ]

        for x in range(102):
            for y in range(40):
                self.console.put_char(x + 1, y + 1, ord(logo[y][x]))


class MainMenu(UIScreen):

    def __init__(self, game: Game) -> None:

        # LOGO
        self.logo_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(bottom = POSITION_RECT.relative_point(1.0, 0.33)[1]),
            subviews = [LogoView()])

        # MAIN MENU
        self.start_button = ButtonView(
            "Start", callback = self.ui_start,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))
        self.new_button = ButtonView(
            "New", callback = self.ui_new,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 6, left = 2)
        )
        self.load_button = ButtonView(
            "Load", callback = self.ui_load,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 4, left = 2)
        )
        self.quit_game_button = ButtonView(
            "Quit Game", callback = self.ui_quit,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 2, left = 2))

        self.menu_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                            right = POSITION_RECT.relative_point(0.66, 1.0)[0] + 1),
            subviews = [
                self.start_button,
                self.new_button,
                self.load_button,
                self.quit_game_button
            ])

        # CHARACTER INFORMATION
        self.character_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(
                top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                left = POSITION_RECT.relative_point(0.33, 1.0)[0] + 1
            ),
            subviews = []
        )

        super().__init__(name = "MAIN MENU", game = game, views = [
            self.logo_box,
            self.menu_box,
            self.character_box,
        ])

    def on_enter(self, *args):
        self.game.storage.read_from_manifest()

    def ui_start(self):
        # self.game.initialize("2021-05-18")
        self.game.initialize()
        self.game.ui.push_screen(self.game.ui.screens['STAGE'])

    def ui_new(self):
        self.game.initialize_creators()
        self.game.ui.push_screen(self.game.ui.screens['NEW WORLD'])

    def ui_load(self):
        print(self.game.storage.manifest_entries)

    def ui_quit(self):
        self.game.ui.quit()

    def cmd_debug_f1(self):
        if not self.game.ui_debug:
            self.logo_box.fg = (255, 0, 0)
            self.menu_box.fg = (255, 0, 0)
            self.character_box.fg = (255, 0, 0)
            self.game.ui_debug = True
        else:
            self.logo_box.fg = (21, 21, 21)
            self.menu_box.fg = (21, 21, 21)
            self.character_box.fg = (21, 21, 21)
            self.game.ui_debug = False
