from __future__ import annotations
from typing import *
from morphism import *
import numpy as np
import tcod

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class CharacterInfo(UIScreen):

    def __init__(self, game: Game) -> None:

        views = [
            RectView(
                layout = Layout.column_left(40).with_updates(bottom=0.3),
                subviews = [
                    LabelView(
                        "Character Info",
                        align_vert = "top",
                        layout = Layout.row_top(0.5).with_updates(left = 2, right = 2, top = 2)
                    )
                ]
            )
        ]
        super().__init__(name="CHARACTER INFO", game=game, views=views)
        self.covers_screen = True

    def cmd_escape(self):
        self.game.ui.pop_screen()
