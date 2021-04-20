from __future__ import annotations
from typing import *
from morphism import *
import tcod

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.engine.core.input import LoopExit

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class StageView(View):

    def __init__(
            self,
            fg=(255, 255, 255),
            bg=(21, 21, 21),
            clear=True,
            *args,
            **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)
        self.fg = fg
        self.bg = bg
        self.clear = clear

    def draw(self):
        self.context.print(Point(1, 1), "Stage Screen")


class Stage(UIScreen):

    def __init__(self, game: Game) -> None:
        views = [StageView(layout=Layout(
            top=0, right=Options.STAGE_PANEL_WIDTH, bottom=Options.STAGE_PANEL_HEIGHT, left=0))]
        super().__init__(name="STAGE", game=game, views=views)
        self.covers_screen = True

    def cmd_escape(self):
        self.game.screens.pop_screen()
