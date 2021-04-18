from __future__ import annotations
from typing import *
from math import floor

from morphism import *
from .base_manager import BaseManager

if TYPE_CHECKING:
    from anathema.core.game import Game


STAGE_PANEL_WIDTH = 96 - 24
STAGE_PANEL_HEIGHT = 64 - 14
STAGE_WIDTH = 128
STAGE_HEIGHT = 128


class CameraManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.width = 32
        self.height = 24
        self.zoom = 2
        self.padding = 5
        self.clamp_x = 16
        self.clamp_y = 12
        self.world_x = 0
        self.world_y = 0

        self._focus_x = 0
        self._focus_y = 0
        self._tile_size = 16

        self.viewport = Rect.centered_at(
            Size(96 - 24, 64 - 14),
            Point(self.game.player.position.x,
                  self.game.player.position.y))

    def compute_size(self):
        self.width = max(self.clamp_x, floor(STAGE_PANEL_WIDTH / 16))
        self.height = max(self.clamp_y, floor(STAGE_PANEL_HEIGHT / 16))
        self.world_x = floor(
            min(max(-self.padding, self._focus_x - self.width // 2),
                max((self.width - STAGE_WIDTH) // -2, self.padding + STAGE_WIDTH - self.width)))
        self.world_y = floor(
            min(max(-self.padding, self._focus_y - self.height // 2),
                max((self.height - STAGE_HEIGHT) // -2, self.padding + STAGE_HEIGHT - self.height)))

    def set_focus(self, x, y):
        self._focus_x = x
        self._focus_y = y
        self.compute_size()

    def set_padding(self, value):
        self.padding = value
        self.compute_size()

    def world_to_screen(self, x, y):
        return {'x': x - self.world_x, 'y': y - self.world_y}

    def screen_to_world(self, x, y):
        return {'x': x + self.world_x, 'y': y + self.world_y}

    def screen_bounds(self):
        return {'x': self.world_x,
                'y': self.world_y,
                'w': self.width,
                'h': self.height}

    def is_in_view(self, world_x, world_y):
        screen = self.world_to_screen(world_x, world_y)
        return (screen['x'] < self.width
                & screen['y'] < self.height
                & screen['x'] >= 0
                & screen['y'] >= 0)
