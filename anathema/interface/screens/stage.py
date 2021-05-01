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
from anathema.engine.core.input import LoopExit
from anathema.engine.world.tile import tile_dt

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class Stage(UIScreen):

    def __init__(self, game: Game) -> None:
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
                )
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

    def cmd_escape(self):
        self.game.screens.pop_screen()
