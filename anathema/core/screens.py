from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

from anathema.utils.debug import debugmethods
from anathema.abstracts import AbstractManager, AbstractScreen
from anathema.screens import MainMenu, Stage

if TYPE_CHECKING:
    from anathema.core import Game


class Screen_1(AbstractScreen):

    name: str = "SCREEN1"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self):
        print("ENTER >> Screen 1")

    def on_exit(self):
        print("Screen 1 >> EXIT")

    def on_update(self, dt) -> None:
        self.handle_input()

    def cmd_confirm(self):
        print("Screen 1 -- COMMAND CONFIRM")
        self.manager.replace_screen('SCREEN2')


class Screen_2(AbstractScreen):

    name: str = "SCREEN2"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self):
        print("ENTER >> Screen 2")

    def on_exit(self):
        print("Screen 2 >> EXIT")

    def on_update(self, dt) -> None:
        self.handle_input()

    def cmd_escape(self):
        print("Screen 2 -- COMMAND ESCAPE")
        self.manager.replace_screen('SCREEN1')


class ScreenManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._stack: List[AbstractScreen] = []
        self._screens: Dict[str, AbstractScreen] = {
            # 'SCREEN1': Screen_1,
            # 'SCREEN2': Screen_2,
            'MAIN MENU': MainMenu,
            'STAGE': Stage,
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
        screen = self._screens[screen](self)
        self._stack.append(screen)
        self.current_screen.on_enter()

    def replace_screen(self, screen: str) -> None:
        """Equivalent to a pop_screen followed by a push_screen."""
        self.current_screen.on_leave()
        self._stack.pop()
        screen = self._screens[screen](self)
        self._stack.append(screen)
        self.current_screen.on_enter()
        self.game.input.change_input_source()

    def push_screen(self, screen: str) -> None:
        """Push a screen onto the top of the stack."""
        self.current_screen.on_leave()
        screen = self._screens[screen](self)
        self._stack.append(screen)
        self.current_screen.on_enter()
        self.game.input.change_input_source()

    def pop_screen(self) -> AbstractScreen:
        """Remove the highest screen from the stack."""
        self.current_screen.on_leave()
        self._stack.pop()
        self.current_screen.on_enter()
        self.game.input.change_input_source()

    def update(self, dt) -> None:
        self.current_screen.on_update(dt)
