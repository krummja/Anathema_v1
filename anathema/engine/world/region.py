from __future__ import annotations
from typing import *

from .world import World

if TYPE_CHECKING:
    pass


class Region:

    def __init__(self, world: World) -> None:
        self.world = world
