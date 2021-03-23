from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

from bearlibterminal import terminal
from anathema.abstracts import AbstractManager, AbstractScreen
from anathema.screens.test import TestScreen

if TYPE_CHECKING:
    from anathema.core import Game


class ScreenManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.should_exit = False
        self._stack: List[AbstractScreen] = []

    @property
    def active_screen(self) -> Optional[AbstractScreen]:
        if self._stack:
            return self._stack[-1]
        else:
            return None

    def replace_screen(self, screen: AbstractScreen):
        if self._stack:
            self.pop_screen(may_exit=False)
        self.push_screen(screen)

    def push_screen(self, screen: AbstractScreen):
        if self.active_screen:
            self.active_screen.resign_active()
        self._stack.append(screen)
        screen.manager = self
        screen.on_enter()
        screen.become_active()
        self.game.input.change_input_source()

    def pop_screen(self, may_exit=True):
        if self.active_screen:
            self.active_screen.resign_active()
        if self._stack:
            last_screen = self._stack.pop()
            last_screen.on_leave()
        if self.active_screen:
            self.active_screen.become_active()
            self.game.input.change_input_source()
        elif may_exit:
            self.should_exit = True

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def quit(self):
        while self._stack:
            self.pop_screen(may_exit=True)

    @staticmethod
    def get_initial_screen():
        return TestScreen()

    def terminal_update(self):
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.terminal_update(screen == self._stack[-1])
        return not self.should_exit

    def terminal_read(self, char):
        if char == terminal.TK_ESCAPE:
            self.quit()
            return True
        if self._stack:
            return self.active_screen.terminal_read(char)
