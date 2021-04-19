from __future__ import annotations
from typing import *

from anathema.engine.core import BaseManager

from anathema.interface import *

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


class ScreenManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self.screens = {
            'MAIN MENU': MainMenu(game),
            'STAGE': Stage(game)
        }
        self._stack: List[Screen] = []
        self.should_continue: bool = True

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
        screen.on_enter()
        screen.become_active()

    def pop_screen(self, may_exit=False):
        if self.active_screen:
            self.active_screen.resign_active()
        if self._stack:
            last_screen = self._stack.pop()
            last_screen.on_leave()
        if self.active_screen:
            self.active_screen.become_active()
        elif may_exit:
            self.should_continue = False

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def update(self):
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.on_update(screen == self._stack[-1])

    def quit(self):
        print("Exiting...")
        while self._stack:
            self.pop_screen(may_exit=True)
