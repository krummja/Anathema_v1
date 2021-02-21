
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
        super().__init__(manager)
        self.game: Game = manager.game
        self.panels = []

    def on_enter(self) -> None:
        self.game.renderer.clear()
        self.game.fov_system.update(100)
        self.game.render_system.update(100)
        self.game.renderer.terminal.refresh()

    def on_draw(self, dt) -> None:
        pos = self.game.player.position
        self.game.renderer.print(1, 1, 0xFFFF00FF, str(pos))
        self.game.renderer.draw_box(65, 1, 30, 62, 0xFFFFFFFF)

    def on_update(self, dt) -> None:
        self.handle_input()
        self.game.update_engine_systems(dt)

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        self.game.player.move((x, y))

    def cmd_escape(self):
        self.game.screens.replace_screen('MAIN MENU')
