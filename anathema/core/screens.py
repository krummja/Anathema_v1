from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Type, Optional

from anathema.abstracts import AbstractManager, AbstractScreen
from anathema.screens.test import TestScreen

if TYPE_CHECKING:
    from anathema.core import Game


class ScreenManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._stack: List[AbstractScreen] = []
        self._screens: Dict[str, Type[AbstractScreen]] = {}

    @property
    def active_screen(self) -> Optional[AbstractScreen]:
        if self._stack:
            return self._stack[-1]
        else:
            return None

    def replace_screen(self, screen: AbstractScreen):
        self.pop_screen()
        self.push_screen(screen)

    def push_screen(self, screen: AbstractScreen):
        if self.active_screen:
            self.active_screen.resign_active()
        self._stack.append(screen)
        screen.manager = self
        screen.on_enter()
        screen.become_active()

    def pop_screen(self):
        if self.active_screen:
            self.active_screen.resign_active()
        if self._stack:
            last_screen = self._stack.pop()
            last_screen.on_leave()
            last_screen.manager = None
        if self.active_screen:
            self.active_screen.become_active()

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def get_initial_screen(self):
        return TestScreen()

    def update(self):
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.on_update(screen == self._stack[-1])
