from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class InputManager(BaseManager):

    def __init__(self, game: BaseGame):
        super().__init__(game)
