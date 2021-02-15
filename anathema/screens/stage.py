
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from enum import Enum

from anathema.abstracts import AbstractScreen, T

if TYPE_CHECKING:
    from anathema.core.screens import Screens
    from anathema.core.game import Game


class Stage(AbstractScreen):

    name: str = "STAGE"

    def __init__(self, manager: Screens) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self) -> None:
        print("Entered Stage")

    def on_leave(self) -> None:
        print("Leaving Stage")

    def on_update(self, dt) -> None:
        self.handle_input()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass
