from __future__ import annotations
from typing import TYPE_CHECKING

import math
from anathema.utils.math_utils import mod
from anathema.utils.geometry import Rect
from anathema.core.options import Options
from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class CameraManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.panel_width = 62
        self.panel_height = 62
        self.camera_bounds = Rect.from_edges(left=0, top=0, right=self.panel_width, bottom=self.panel_height)
        self.render_offset = {'x': 0, 'y': 0}

    def position_camera(self):
        range_width: int = max(0, Options.STAGE_WIDTH - self.panel_width)
        range_height: int = max(0, Options.STAGE_HEIGHT - self.panel_height)

        camera_range = Rect.from_edges(left=0, top=0, right=range_width, bottom=range_height)

        player_pos = self.game.player.position

        camera_view = {
            'x': player_pos[0] - mod(self.panel_width, 4),
            'y': player_pos[1] - mod(self.panel_height, 2)
            }

        camera_view = camera_range.clamp(camera_view['x'], camera_view['y'])

        self.camera_bounds = Rect.from_edges(
            left=camera_view[0],
            top=camera_view[1],
            right=min(self.panel_width, Options.STAGE_WIDTH),
            bottom=min(self.panel_height, Options.STAGE_HEIGHT)
            )

        self.render_offset = {
            'x': max(0, self.panel_width - Options.STAGE_WIDTH)// 4,
            'y': max(0, self.panel_height - Options.STAGE_HEIGHT)// 2
            }

    def update(self, dt):
        self.position_camera()
