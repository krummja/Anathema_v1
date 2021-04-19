from __future__ import annotations
from typing import *
import numpy as np

from anathema.engine.core import BaseManager
from anathema.engine.core.options import Options

if TYPE_CHECKING:
    from anathema.engine.world.area import Area
    from anathema.engine.core.game import Game


class CameraManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._camera_pos: Tuple[int, int] = (0, 0)

    @property
    def current_area(self) -> Area:
        return self.game.world.current_area

    @property
    def camera_pos(self) -> Tuple[int, int]:
        cam_x = self._camera_pos[0] - Options.STAGE_PANEL_WIDTH // 2
        cam_y = self._camera_pos[1] - Options.STAGE_PANEL_HEIGHT // 2
        return cam_x, cam_y

    @property
    def camera_view(self) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        cam_x, cam_y = self.camera_pos

        screen_left = max(0, -cam_x)
        screen_top = max(0, -cam_y)
        world_left = max(0, cam_x)
        world_top = max(0, cam_y)

        screen_width = min(Options.STAGE_PANEL_WIDTH - screen_left, self.current_area.width - world_left)
        screen_height = min(Options.STAGE_PANEL_HEIGHT - screen_top, self.current_area.height - world_top)

        screen_view = np.s_[screen_top:screen_top+screen_height, screen_left:screen_left+screen_width]
        world_view = np.s_[world_top:world_top+screen_height, world_left:world_left+screen_width]

        return screen_view, world_view
