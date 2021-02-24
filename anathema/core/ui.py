from __future__ import annotations
import enum
from typing import TYPE_CHECKING, Tuple, Optional
from enum import Enum

from collections import deque

import tcod
from anathema.abstracts import AbstractManager
from anathema.core.options import Options
from anathema.utils.geometry import Rect, Point, Size

if TYPE_CHECKING:
    from tcod.bsp import BSP
    from anathema.core.game import Game


class UIManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.data_list = []

    def push_data(self, data):
        self.data_list.append(data)

    def clear_data(self):
        self.data_list.clear()
