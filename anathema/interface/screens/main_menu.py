from __future__ import annotations
from typing import *
import numpy as np
import tcod

from morphism import *

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView
from anathema.engine.core.input import LoopExit

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


POSITION_RECT = Rect(Point(0, 0), Size(Options.CONSOLE_WIDTH, Options.CONSOLE_HEIGHT))


class LogoView(View):

    def draw(self):
        self.console.clear()
        anathema_logo = tcod.image_load('logo.png')
        print(anathema_logo)
        # anathema_logo.set_key_color((21, 21, 21))
        anathema_logo.blit(self.console, 2, 2, tcod.BKGND_SET, 1.0, 1.0, 0.0)


class MainMenu(UIScreen):

    def __init__(self, game: Game) -> None:

        self.logo_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(top = 0, left = 0, right = 0, bottom = POSITION_RECT.relative_point(1.0, 0.66)[1]),
            subviews = []
        )

        self.menu_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(
                top = POSITION_RECT.relative_point(1.0, 0.33)[1] + 1,
                right = POSITION_RECT.relative_point(0.66, 1.0)[0] + 1,
                bottom = 0,
                left = 0
            ),
            subviews = [
                ButtonView(
                    "Start",
                    callback = self.ui_start,
                    align_horz = "left", align_vert = "bottom",
                    layout = Layout(left = 2, bottom = 8)
                ),
                ButtonView(
                    "New Character",
                    callback = lambda: None,
                    align_horz = "left", align_vert = "bottom",
                    layout = Layout(left = 2, bottom = 6)
                ),
                ButtonView(
                    "Load Character",
                    callback = lambda: None,
                    align_horz = "left", align_vert = "bottom",
                    layout = Layout(left = 2, bottom = 4)
                ),
                ButtonView(
                    "Quit Game",
                    callback = self.ui_quit,
                    align_horz = "left", align_vert = "bottom",
                    layout = Layout(left = 2, bottom = 2)
                )
            ]
        )

        self.active_character_label = LabelView(
            "", align_horz = "left", layout = Layout.row_top(1.0).with_updates(left = 2, top = 2, right = 0)
        )
        self.character_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(
                top = POSITION_RECT.relative_point(1.0, 0.33)[1] + 1,
                right = 0,
                bottom = 0,
                left = POSITION_RECT.relative_point(0.33, 1.0)[0] + 1
            ),
            subviews = [
                self.active_character_label
            ]
        )

        views = [
            self.logo_box,
            self.menu_box,
            self.character_box
        ]
        super().__init__(name = "MAIN MENU", game = game, views = views)

    def post_update(self):
        if self.game.storage.active_character:
            name = self.game.storage.active_character["name"]
            self.active_character_label.update(name)

    def ui_start(self):
        self.game.world.initialize()
        if not self.game.hot_start:
            self.game.player.initialize()
            self.game.hot_start = True
        self.game.screens.push_screen(self.game.screens.screens['STAGE'])

    def ui_generate(self):
        self.game.screens.push_screen(self.game.screens.screens['WORLD GEN'])

    def ui_quit(self):
        self.game.screens.quit()

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
