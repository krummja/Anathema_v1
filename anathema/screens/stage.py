from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from anathema.core.options import Options
from anathema.abstracts import AbstractScreen, T

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager
    from anathema.core.game import Game


class Stage(AbstractScreen):

    name: str = "STAGE"

    def __init__(self, manager: ScreenManager) -> None:
        """Base extensible screen for use inside the game loop."""
        super().__init__(manager)
        self.game: Game = manager.game

    def on_update(self, dt) -> None:
        self.handle_input()
