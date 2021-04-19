from __future__ import annotations
from typing import *
import tcod

from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.engine.core.input import LoopExit

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class MainMenu(UIScreen):

    def __init__(self, game: BaseGame) -> None:
        views = [RectView(layout=Layout(top=2, right=2, bottom=2, left=2),
                          subviews=[
                              LabelView("Test", align_vert="top", align_horz="left",
                                        layout=Layout(left=10, top=10))
                          ])]
        super().__init__(name="MAIN MENU", game=game, views=views)

    def cmd_escape(self):
        self.game.screens.quit()

    def cmd_return(self):
        self.game.screens.push_screen(self.game.screens.screens['STAGE'])
