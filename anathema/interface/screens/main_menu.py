from __future__ import annotations
from typing import *
import numpy as np
import tcod

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView
from anathema.engine.core.input import LoopExit

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class LogoView(View):

    def draw(self):
        logo = np.array([
            "    █      ",
            "     █     ",
            "  █████    ",
            "    ███    ",
            "    █ ██   ",
            "   █  ██   ",
            "  ███████  ",
            "  █    ██  ",
            " █     ███ ",
            "████  █████",
        ])
        logo = np.array([list(line) for line in logo])
        height = logo.shape[0]
        vertical_offset = 4
        _y = 0
        for line in logo:
            width = len(line)
            _x = 0
            if _y <= height:
                for char in line:
                    if _x <= width:
                        self.console.print((Options.CONSOLE_WIDTH - width) // 2 + _x,
                                           vertical_offset + _y, char, fg = (255, 255, 255))
                        _x += 1
                _y += 1


class MainMenu(UIScreen):

    def __init__(self, game: Game) -> None:
        views = [
            RectView(fg=(21, 21, 21), layout=Layout(top=0, right=0, bottom=0, left=0),
                     subviews=[
                         ButtonView("Start",
                                    callback=self.start,
                                    align_horz="left",
                                    layout=Layout(left=10, top=0)),

                         ButtonView("New World",
                                    callback=self.generate,
                                    align_horz="left",
                                    layout=Layout(left=10, top=4)),

                         ButtonView("Quit",
                                    callback=self.quit,
                                    align_horz="left",
                                    layout=Layout(left=10, top=8)),
                     ])
        ]
        super().__init__(name="MAIN MENU", game=game, views=views)

    def start(self):
        self.game.world.initialize()
        self.game.player.initialize()
        self.game.screens.push_screen(self.game.screens.screens['STAGE'])

    def generate(self):
        self.game.screens.push_screen(self.game.screens.screens['WORLD GEN'])

    def quit(self):
        self.game.screens.quit()
