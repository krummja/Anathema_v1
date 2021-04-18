from __future__ import annotations
from typing import *
import tcod

from .base_manager import BaseManager
from anathema.screens.test_screen import TestScreen

if TYPE_CHECKING:
    from anathema.screens.screen import Screen
    from anathema.core.game import Game


class ScreenManager(BaseManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._stack: List[Screen] = []
        self._should_continue: bool = True

    @property
    def active_screen(self) -> Optional[Screen]:
        if self._stack:
            return self._stack[-1]
        return None

    def replace_screen(self, screen: Screen):
        if self._stack:
            self.pop_screen(may_exit=False)
        self.push_screen(screen)

    def push_screen(self, screen: Screen):
        if self.active_screen:
            self.active_screen.resign_active()
        self._stack.append(screen)
        screen.manager = self
        screen.on_enter()
        screen.become_active()

    def pop_screen(self, may_exit=True):
        if self.active_screen:
            self.active_screen.resign_active()
        if self._stack:
            last_screen = self._stack.pop()
            last_screen.on_leave()
        if self.active_screen:
            self.active_screen.become_active()
        elif may_exit:
            self._should_continue = False

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def get_initial_screen(self):
        return TestScreen()

    def quit(self):
        while self._stack:
            self.pop_screen(may_exit=True)
