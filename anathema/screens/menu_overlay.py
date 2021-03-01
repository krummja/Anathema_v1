from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.screens.player_ready import PlayerReady

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class MenuOverlay(PlayerReady):
    """Extensible base screen for creating menus."""

    name: str = ""

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.selection = (0, 0)

    def on_draw(self, dt) -> None:
        super().on_draw(dt)

    def cmd_escape(self) -> None:
        self.game.screens.pop_screen()

