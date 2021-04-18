from __future__ import annotations
import tcod
from anathema.screens.screen import UIScreen
from screens.views.view import Layout
from anathema.screens.views.test_view import TestView


class TestScreen(UIScreen):

    def __init__(self):
        views = TestView(layout=Layout(left=0, top=0, right=0, bottom=0))
        super().__init__(views)
        self.covers_screen = True

    def become_active(self):
        self.view.perform_draw(self.manager.game.console.root_console)
        self.manager.game.systems_update(100)

    def handle_input(self, event):
        if event.sym == tcod.event.K_ESCAPE:
            self.manager.game.screens.pop_screen()
