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
from anathema.engine.data.spawner import spawn

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class Stage(UIScreen):

    def __init__(self, game: Game) -> None:

        self.player_energy = 0.0

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
                    BarGaugeView(
                        text = str(self.player_energy),
                        label="Player",
                        fullness = self.player_energy / -2000,
                        fg = (50, 50, 255),
                        layout = Layout(
                            top = 2, left = 2, bottom = None, right = None,
                            height = 1, width = 20
                        )
                    )
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
        self.game.player_update()

    def post_update(self):
        self.player_energy = self.game.player.entity['Actor'].energy

    def cmd_escape(self):
        self.game.screens.push_screen(EscapeMenu(self.game))

    def cmd_character_info(self):
        self.game.screens.push_screen(self.game.screens.screens['CHARACTER INFO'])

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
        self.game.teardown()
        self.game.screens.replace_screen(self.game.screens.screens['MAIN MENU'])

    def ui_exit_game(self):
        pass

    def cmd_escape(self):
        self.game.screens.pop_screen()
