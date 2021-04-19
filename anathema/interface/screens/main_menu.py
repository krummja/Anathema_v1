from __future__ import annotations
from typing import *
import tcod

from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView
from anathema.engine.core.input import LoopExit

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class MainMenu(UIScreen):

    def __init__(self, game: BaseGame) -> None:
        views = [
            RectView(layout=Layout(top=0, right=0, bottom=0, left=0))
                 ]
        super().__init__(name="MAIN MENU", game=game, views=views)

    def create(self):
        pass

    def cmd_escape(self):
        self.game.screens.quit()

    def cmd_return(self):
        self.game.screens.push_screen(self.game.screens.screens['STAGE'])
