from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from anathema.core.options import Options
from anathema.utils.debug import debugmethods
from anathema.abstracts import AbstractScreen, T, StateBreak
from clubsandwich.geom import Point

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager
    from anathema.core.game import Game


class MainMenu(AbstractScreen):

    name: str = "MAIN MENU"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game
        self.panels = []

    def on_enter(self) -> None:
        self.game.renderer.clear()
        self.game.renderer.refresh()

    def on_leave(self) -> None:
        pass

    def on_draw(self, dt) -> None:
        self.game.renderer.clear()
        self.game.renderer.print(1, 1, 0xFFFF00FF, "test string")

    def on_update(self, dt) -> None:
        self.handle_input()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_next(self) -> Optional[T]:
        self.game.ui.next_panel()

    def cmd_confirm(self) -> Optional[T]:
        self.manager.replace_screen('STAGE')

    def cmd_escape(self) -> None:
        raise SystemExit()
