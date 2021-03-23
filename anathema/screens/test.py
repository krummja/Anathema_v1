from __future__ import annotations

from anathema.abstracts.screen import UIScreen
from anathema.abstracts.view import LayoutOptions
from anathema.screens.views.window_view import WindowView
from anathema.screens.views.label_view import LabelView


class TestScreen(UIScreen):

    name: str = "Test"

    def __init__(self, *args, **kwargs):
        view = WindowView(
            'Test',
            layout_options=LayoutOptions(top=1, right=1, bottom=1, left=1))
        super().__init__(view, *args, **kwargs)
        self.covers_screen = True

    def become_active(self):
        self.game.renderer.clear()

    def quit(self):
        self.manager.pop_screen()


class TestScreen2(UIScreen):

    name: str = "Test2"

    def __init__(self, *args, **kwargs):
        views = []
        super().__init__(views, *args, **kwargs)

    def quit(self):
        self.manager.pop_screen()
