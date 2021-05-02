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


class WorldGen(UIScreen):

    debug = True

    def __init__(self, game: Game):
        views = [
            RectView(
                layout = Layout(
                    left = Options.STAGE_PANEL_WIDTH,
                )
            )
        ]
        super().__init__(name="WORLD GEN", game=game, views=views)

        # FIXME Don't like setting this ad hoc like this...
        Options.STAGE_PANEL_HEIGHT = Options.CONSOLE_HEIGHT
        self.covers_screen = True
        self.position = (0, 0)

    def on_enter(self):
        self.game.console.root.clear()

    def cmd_escape(self):
        self.game.screens.pop_screen()

    def pre_update(self):
        self.game.render_system.draw_world_map()

    def post_update(self):
        if self.debug:
            self.debug_data()

    def move_focus(self, direction):
        WIDTH = self.game.world.generator.width
        HEIGHT = self.game.world.generator.height

        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]
        if 0 <= target_x < WIDTH and 0 <= target_y < HEIGHT:
            self.position = (target_x, target_y)
            self.game.camera.camera_pos = self.position

    def debug_data(self):
        self.game.console.root.print(
            Options.STAGE_PANEL_WIDTH + 2, 2,
            "Height:   " + str(self.game.world.generator.heightmap.array[self.position[1], self.position[0]]))
        self.game.console.root.print(
            Options.STAGE_PANEL_WIDTH + 2, 4,
            "Position: " + str(self.position))
