from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

from anathema.abstracts import AbstractManager, AbstractScreen
from anathema.screens import MainMenu, PlayerReady, MenuOverlay
from anathema.utils.observer import Observer

if TYPE_CHECKING:
    from anathema.core.ui import UIManager
    from anathema.core import Game


class ScreenManager(AbstractManager, Observer):

    def __init__(self, game: Game) -> None:
        AbstractManager.__init__(self, game)
        Observer.__init__(self)

        self.game.ui.attach(self)

        self._stack: List[AbstractScreen] = [MainMenu(self)]
        self._screens: Dict[str, AbstractScreen] = {
            'MAIN MENU': MainMenu,
            'PLAYER READY': PlayerReady,
            'MENU OVERLAY': MenuOverlay
            }

    @property
    def current_screen(self) -> AbstractScreen:
        if len(self._stack) > 0:
            return self._stack[-1]

    def set_screen(self, screen: str) -> None:
        """Dump the current stack if there is one and push a new screen."""
        while len(self._stack) > 0:
            self.current_screen.on_leave()
            self._stack.pop()
        screen = self._screens[screen](self)
        self._stack.append(screen)
        self.current_screen.on_enter()

    def replace_screen(self, screen: str, *args) -> None:
        """Equivalent to a pop_screen followed by a push_screen."""
        self.current_screen.on_leave()
        self._stack.pop()
        screen = self._screens[screen](self)
        self._stack.append(screen)
        self.current_screen.on_enter(*args)
        self.game.input.change_input_source()

    def push_screen(self, screen: str, *args) -> None:
        """Push a screen onto the top of the stack."""
        self.current_screen.on_leave()
        screen = self._screens[screen](self)
        self._stack.append(screen)
        self.current_screen.on_enter(*args)
        self.game.input.change_input_source()

    def pop_screen(self) -> AbstractScreen:
        """Remove the highest screen from the stack."""
        self.current_screen.on_leave()
        self._stack.pop()
        self.current_screen.on_enter()
        self.game.input.change_input_source()

    def _update(self, subject: UIManager) -> None:
        self.push_screen('MENU OVERLAY', 'interactions', subject.data)

    def update(self, dt) -> None:
        self.current_screen.on_update(dt)
        self.game.renderer.push_to_stack(self.current_screen.on_draw)
