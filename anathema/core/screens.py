from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

from anathema.abstracts import AbstractManager, AbstractScreen
from anathema.screens import MainMenu, Stage

if TYPE_CHECKING:
    from anathema.core import Game


class ScreenManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._stack: List[AbstractScreen] = []
        self._screens: Dict[str, AbstractScreen] = {
            'MAIN MENU': MainMenu(self),
            'STAGE': Stage(self),
        }
        self.set_screen('MAIN MENU')

    @property
    def current_screen(self) -> AbstractScreen:
        return self._stack[-1]

    def set_screen(self, screen: str) -> None:
        """Dump the current stack if there is one and push a new screen."""
        while len(self._stack) > 0:
            self.current_screen.on_leave()
            self._stack.pop()
        self._stack.append(self._screens[screen])
        self.current_screen.on_enter()

    def replace_screen(self, screen: str) -> None:
        """Equivalent to a pop_screen followed by a push_screen."""
        self.current_screen.on_leave()
        self._stack.pop()
        self._stack.push(self._screens[screen])
        self.current_screen.on_enter()

    def push_screen(self, screen: str) -> None:
        """Push a screen onto the top of the stack."""
        self.current_screen.on_leave()
        self._stack.append(self._screens[screen])
        self.game.input._current_screen = self.current_screen
        self.current_screen.on_enter()

    def pop_screen(self) -> AbstractScreen:
        """Remove the highest screen from the stack."""
        self.current_screen.on_leave()
        self._stack.pop()
        self.current_screen.on_enter()

    def update(self, dt) -> None:
        self.current_screen.on_update(dt)
