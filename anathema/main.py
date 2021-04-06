from __future__ import annotations
import nocterminal as noc
from morphism import *


class StartScreen(noc.ui.AbstractScreen):

    name = "Start Screen"

    def terminal_update(self, is_active=False):
        self.director.context.print(Point(1, 1), "Test")
        return True

    def terminal_read(self, char):
        if char == noc.terminal.TK_ENTER:
            self.director.push_screen(MainScreen(self.director))
        if char == noc.terminal.TK_ESCAPE:
            self.director.pop_screen(may_exit=True)


class MainScreen(noc.ui.AbstractScreen):

    name = "Main Screen"

    def terminal_update(self, is_active=False):
        self.director.core.engine_update()
        self.director.context.print(Point(1, 10), "MainScreen Test!")
        return True

    def terminal_read(self, char):
        if char == noc.terminal.TK_ESCAPE:
            self.director.pop_screen()


class Game(noc.CoreLoop):

    def __init__(self):
        super().__init__()

    def get_initial_screen(self):
        return StartScreen(self.director)

    def systems_init(self):
        pass

    def systems_update(self):
        pass


if __name__ == '__main__':
    Game().start()
