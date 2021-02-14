from __future__ import annotations
from typing import TYPE_CHECKING
from bearlibterminal import terminal

from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class Renderer(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.config = "../terminal.ini"
        self._terminal = terminal

    @property
    def terminal(self) -> terminal:
        return self._terminal

    def clear(self) -> None:
        self._terminal.clear()
        self._terminal.bkcolor(0xFF2A2A2A)

    def setup(self) -> None:
        self._terminal.open()
        self._terminal.composition(True)
        self._terminal.refresh()

    def teardown(self) -> None:
        self._terminal.composition(False)
        self._terminal.close()
