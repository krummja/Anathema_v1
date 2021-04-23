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


class StageView(View):

    def __init__(
            self,
            fg=(255, 255, 255),
            bg=(21, 21, 21),
            clear=False,
            *args,
            **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)
        self.fg = fg
        self.bg = bg
        self.clear = clear
        self.fill = False

    def draw(self):
        pass
        # self.screen.game.console.root.tiles_rgb[:] = (ord("#"), [100, 0, 100], [21, 21, 21])
        # self.context.print(Point(10, 10), "Hello, world!", fg=(255, 255, 255))


class Stage(UIScreen):

    def __init__(self, game: Game) -> None:
        views = [StageView(layout=Layout(
            top=0, right=Options.STAGE_PANEL_WIDTH, bottom=Options.STAGE_PANEL_HEIGHT, left=0))]
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
