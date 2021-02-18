
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from anathema.abstracts import AbstractScreen, T

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager
    from anathema.core.game import Game


class Stage(AbstractScreen):

    name: str = "STAGE"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self) -> None:
        self.game.fov_system.update(100)
        self.game.render_system.update(100)

    def on_update(self, dt) -> None:
        self.on_draw(dt)
        self.handle_input()
        self.game.update_engine_systems(dt)

    def on_draw(self, dt) -> None:
        ui = self.game.ui
        for panel in ui.panels:
            panel.draw()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        self.game.player.move((x, y))

    def cmd_escape(self):
        self.game.screens.replace_screen('MAIN MENU')
