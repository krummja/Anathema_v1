from __future__ import annotations
from typing import TYPE_CHECKING
from bearlibterminal import terminal

from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core.game import Game


class RenderManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
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
        self._terminal.bkcolor(0xFF2A2A2A)

    def teardown(self) -> None:
        self._terminal.composition(False)
        self._terminal.close()

    def fill(self, char: str = "█", color: int = 0xFF2A2A2A) -> None:
        self._terminal.layer(0)
        self._terminal.color(color)

        for x in range(96):
            for y in range(64):
                self._terminal.put(x, y, char)
