from __future__ import annotations
from typing import *
from morphism import *
import numpy as np
import tcod
import copy
import random

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView
from anathema.interface.views.bar_gauge import BarGaugeView
from anathema.interface.views.simple_list import SimpleListView
from anathema.engine.data.spawner import spawn

from anathema.data import Storage

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class Stage(UIScreen):

    def __init__(self, game: Game) -> None:

        self.health_gauge = BarGaugeView(
            text = "", label = "Health",
            fullness = 1.0, fg = (255, 50, 50),
            layout = Layout(top = 2, left = 2, bottom = None, right = None, height = 1, width = 20)
        )

        self.exp_gauge = BarGaugeView(
            text = "", label = "Exp.",
            fullness = 1.0, fg = (255, 180, 0),
            layout = Layout(top = 4, left = 2, bottom = None, right = None, height = 1, width = 20)
        )

        views = [
            RectView(
                layout=Layout(
                    right = Options.CONSOLE_WIDTH-Options.STAGE_PANEL_WIDTH,
                    top = Options.STAGE_PANEL_HEIGHT
                )
            ),
            RectView(
                layout = Layout(
                    left = Options.STAGE_PANEL_WIDTH,
                ),
                subviews = [
                    self.health_gauge,
                    self.exp_gauge
                ]
            )
        ]

        super().__init__(name="STAGE", game=game, views=views)
        self.covers_screen = True

    def on_enter(self, *args):
        self.game.console.root.clear()
        self.game.camera.camera_pos = self.game.player.position
        self.game.fov_system.update_fov()
        self.game.render_system.update()

    def pre_update(self):
        self.game.engine_update()

    def post_update(self):
        pass

    def cmd_escape(self):
        self.game.ui.push_screen(EscapeMenu(self.game))

    def cmd_character_info(self):
        self.game.ui.push_screen(self.game.ui.screens['CHARACTER INFO'])

    def cmd_spawn(self):
        roll = random.randrange(0, 100)
        if roll >= 50:
            offset = 1
        else:
            offset = -1
        x, y = self.game.player.position
        spawn(self.game, 'SPAWN_WANDERER', x + offset, y)


class EscapeMenu(UIScreen):

    def __init__(self, game: Game) -> None:

        views = [
            RectView(
                layout = Layout(left = 44, right = 44, top = 23, bottom = 33),
                subviews = [
                    ButtonView(
                        "Options", callback = None,
                        align_vert = "top",
                        layout = Layout(left = 2, right = 2, top = 2)
                    ),
                    ButtonView(
                        "Quit to Main", callback = self.ui_quit_to_menu,
                        align_vert = "top",
                        layout = Layout(left = 2, right = 2, top = 4)
                    ),
                    ButtonView(
                        "Exit Game", callback = self.ui_exit_game,
                        align_vert = "top",
                        layout = Layout(left = 2, right = 2, top = 6)
                    ),
                ]
            )
        ]

        super().__init__(name="ESCAPE MENU", game=game, views=views)
        self.covers_screen = True

    def ui_quit_to_menu(self):
        # self.game.storage.write_to_file()
        self.game.teardown()
        self.game.ui.replace_screen(self.game.ui.screens['MAIN MENU'])

    def ui_exit_game(self):
        pass

    def cmd_escape(self):
        self.game.ui.pop_screen()
