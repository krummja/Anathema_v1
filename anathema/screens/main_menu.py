from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from enum import Enum

from anathema.abstracts import AbstractScreen, T

if TYPE_CHECKING:
    from anathema.core.screens import Screens
    from anathema.core.game import Game


class MainMenu(AbstractScreen):

    name: str = "MAIN MENU"

    def __init__(self, manager: Screens) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self) -> None:
        print("Entered Main Menu")

    def on_leave(self) -> None:
        self.game.renderer.clear()
        print("Leaving Main Menu")

    def on_update(self, dt) -> None:
        self.on_draw(100)
        self.handle_input()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_confirm(self) -> Optional[T]:
        print("ENTER PRESSED!")
        self.manager.push_screen('STAGE')

    def cmd_escape(self) -> None:
        self.cmd_quit()

    def on_draw(self, dt) -> None:
        self.game.renderer.fill()
        self.game.renderer.terminal.layer(1)
        self.game.renderer.terminal.color(0xFFFFFFFF)
        self.game.renderer.terminal.puts(1, 1, "Hello world!")

