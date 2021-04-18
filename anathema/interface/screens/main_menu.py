from __future__ import annotations
from typing import *

from anathema.interface.screens import UIScreen

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class MainMenu(UIScreen):

    def __init__(self, game: BaseGame) -> None:
        super().__init__(name="MAIN MENU", game=game)
