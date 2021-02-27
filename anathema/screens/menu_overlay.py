from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.screens import PlayerReady

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class MenuOverlay(PlayerReady):
    """Extensible base screen for creating menus."""

    name: str = ""

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)

    def on_draw(self, dt) -> None:
        pass

    def cmd_escape(self) -> None:
        self.game.screens.pop_screen()

