from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from anathema.utils.debug import debugmethods
from anathema.abstracts import AbstractScreen, T, StateBreak
from clubsandwich.geom import Point

if TYPE_CHECKING:
    from anathema.core.screens import Screens
    from anathema.core.game import Game


@debugmethods
class MainMenu(AbstractScreen):

    name: str = "MAIN MENU"

    def __init__(self, manager: Screens) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self) -> None:
        self.game.ui.split()

    def on_leave(self) -> None:
        self.game.renderer.clear()

    def on_update(self, dt) -> None:
        self.on_draw(100)
        self.handle_input()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_next(self) -> Optional[T]:
        self.game.ui.next_panel()

    def cmd_confirm(self) -> Optional[T]:
        self.manager.push_screen('STAGE')

    def cmd_escape(self) -> None:
        raise StateBreak()

    def on_draw(self, dt) -> None:
        ui = self.game.ui

        self.game.renderer.clear()
        self.game.renderer.fill()
        self.game.renderer.terminal.layer(1)
        self.game.renderer.terminal.color(0xFFFFFFFF)
        for panel in ui.panels:
            panel.draw()
        self.game.renderer.terminal.refresh()
